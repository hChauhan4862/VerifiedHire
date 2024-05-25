// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract UserManagement {
    // Enums for user status, type, and gender
    enum UserStatus {
        Registered,
        Approved,
        Deactivated
    }
    enum UserType {
        Admin,
        Organization,
        Employee
    }
    enum Gender {
        Male,
        Female,
        Other
    }

    // Structs for user information and status
    struct User {
        string name;
        string email;
        Gender gender;
        string phone;
        UserType userType;
    }

    struct StatusHistory {
        UserStatus status;
        uint256 timestamp;
        string reason;
        string updatedBy; // Email of the user who updated the status or it can be the system
    }

    struct CreditHistory {
        int256 previousBalance;
        int256 creditChange;
        int256 newBalance;
        string txnComment;
        string updatedBy;
        uint256 updateTimestamp;
    }

    struct SessionData {
        string email;
        uint256 loginTime;
        uint256 logoutTime;
        bool isSessionActive;
    }

    // Mappings to store user data and histories
    mapping(string => User) public userDetails; // Maps email to User details
    mapping(string => UserStatus) public userCurrentStatus; // Maps email to current status
    mapping(string => string) public userPasswords; // Maps email to user password
    mapping(string => StatusHistory[]) public userStatusHistory; // Maps email to status history
    mapping(string => int256) public userCurrentCredits; // Maps email to user credits
    mapping(string => CreditHistory[]) public userCreditHistory; // Maps email to user credits history
    mapping(string => string) public userCurrentAddress; // Maps email to user address
    mapping(string => string) public userProfilePic; // Maps email to user profile picture
    mapping(string => SessionData) public userSessions; // Maps session_id to SessionData
    string[] public registeredUserEmails; // Array to keep track of registered user emails

    // Events for logging actions
    event StatusChanged(
        string email,
        UserStatus previousStatus,
        UserStatus newStatus,
        uint256 timestamp,
        string reason,
        string updatedBy
    );
    event CreditsUpdated(
        string email,
        int256 previousBalance,
        int256 newBalance,
        string txnComment,
        uint256 timestamp,
        string updatedBy
    );
    event NewUserRegistered(
        string email,
        string name,
        UserType userType,
        uint256 timestamp
    );

    // Modifier to check if a user exists
    modifier userExists(string memory email) {
        require(
            bytes(userDetails[email].email).length != 0,
            "User not registered"
        );
        _;
    }

    // Modifier to check if the caller is an admin
    modifier isAdmin(string memory email) {
        require(userDetails[email].userType == UserType.Admin, "Unauthorized");
        _;
    }

    // Modifier to check if the caller is an organization
    modifier isOrganization(string memory email) {
        require(
            userDetails[email].userType == UserType.Organization,
            "Unauthorized"
        );
        _;
    }

    // Modifier to check if the caller is an organization or admin
    modifier isOrganizationOrAdmin(string memory email) {
        require(
            userDetails[email].userType == UserType.Organization ||
                userDetails[email].userType == UserType.Admin,
            "Unauthorized"
        );
        _;
    }

    // Modifier to check if the caller is an employee
    modifier isEmployee(string memory email) {
        require(
            userDetails[email].userType == UserType.Employee,
            "Unauthorized"
        );
        _;
    }

    // Function to register a new user
    function registerUser(
        string memory name,
        string memory email,
        Gender gender,
        string memory phone,
        UserType userType,
        string memory password
    ) public {
        require(
            bytes(userDetails[email].email).length == 0,
            "User already registered"
        );

        User memory newUser = User({
            name: name,
            email: email,
            gender: gender,
            phone: phone,
            userType: userType
        });

        userDetails[email] = newUser;
        userCurrentStatus[email] = UserStatus.Registered;
        userPasswords[email] = password;
        userCurrentCredits[email] = 0;
        registeredUserEmails.push(email);

        // Set initial status and credits
        _setStatus(email, UserStatus.Registered, "User registered", "System");

        if (userType != UserType.Employee){
            _updateCredits(email, 1000, "Registration Bonus", "System");   
        }

        // Emit New User Registered event
        emit NewUserRegistered(email, name, userType, block.timestamp);
    }

    // Function to check if a user exists
    function doesUserExist(string memory email) public view returns (bool) {
        return bytes(userDetails[email].email).length != 0;
    }

    // Function to list all users
    function listAllUsers() public view returns (User[] memory) {
        uint256 userCount = registeredUserEmails.length;
        User[] memory userList = new User[](userCount);
        for (uint256 i = 0; i < userCount; i++) {
            userList[i] = userDetails[registeredUserEmails[i]];
        }
        return userList;
    }

    function getUser(string memory email) public view returns (User memory){
        return userDetails[email];
    }

    // Function to login a user
    function login(
        string memory email,
        string memory password,
        string memory session_id,
        UserType role
    ) public userExists(email) returns (bool) {
        require(
            keccak256(abi.encodePacked(userPasswords[email])) ==
                keccak256(abi.encodePacked(password)),
            "Invalid password"
        );
        require(
            userCurrentStatus[email] == UserStatus.Approved,
            "User not approved"
        );

        require(
            userDetails[email].userType == role
        );

        userSessions[session_id] = SessionData({
            email: email,
            loginTime: block.timestamp,
            logoutTime: 0,
            isSessionActive: true
        });
        return true;
    }

    struct Profile {
        UserManagement.User User;
        UserManagement.StatusHistory[] history_status;
        UserManagement.CreditHistory[] history_credit;
    }

    function getUserProfile(
        string memory email
    ) public view returns (Profile memory) {
        UserManagement.User memory user = getUser(email);
        return Profile(user, getStatusHistory(email), getCreditHistory(email));
    }

    // Function to logout a user
    function logout(string memory session_id) public {
        require(
            userSessions[session_id].isSessionActive,
            "Session already logged out"
        );
        userSessions[session_id].logoutTime = block.timestamp;
        userSessions[session_id].isSessionActive = false;
    }

    // Function to check if a session is active
    function isSessionActive(
        string memory session_id
    ) public view returns (bool) {
        return userSessions[session_id].isSessionActive;
    }

    function sessionData(
        string memory session_id
    ) public view returns (string memory) {
        require(
            userSessions[session_id].isSessionActive,
            "Session already logged out"
        );

        return userSessions[session_id].email;
    }

    // Internal function to set user status
    function _setStatus(
        string memory email,
        UserStatus newStatus,
        string memory reason,
        string memory updatedBy
    ) internal userExists(email) {
        UserStatus previousStatus = userCurrentStatus[email];
        userCurrentStatus[email] = newStatus;

        // Log status change in history
        userStatusHistory[email].push(
            StatusHistory({
                status: newStatus,
                timestamp: block.timestamp,
                reason: reason,
                updatedBy: updatedBy
            })
        );

        // Emit event
        emit StatusChanged(
            email,
            previousStatus,
            newStatus,
            block.timestamp,
            reason,
            updatedBy
        );
    }

    // Function to update user details
    function updateUserDetails(
        string memory email,
        string memory name,
        Gender gender,
        string memory phone,
        UserType userType
    ) public userExists(email) {
        userDetails[email].name = name;
        userDetails[email].gender = gender;
        userDetails[email].phone = phone;
        userDetails[email].userType = userType;
    }

    // Function to change user password
    function changePassword(
        string memory email,
        string memory newPassword
    ) public userExists(email) {
        require(
            keccak256(abi.encodePacked(userDetails[email].email)) ==
                keccak256(abi.encodePacked(email)),
            "Unauthorized"
        ); // Redundant check
        userPasswords[email] = newPassword;
    }

    // Function to deactivate a user
    function deactivateUser(
        string memory email,
        string memory reason,
        string memory updatedBy
    ) public userExists(email) {
        _setStatus(email, UserStatus.Deactivated, reason, updatedBy);
    }

    // Function to activate a user
    function activateUser(
        string memory email,
        string memory reason,
        string memory updatedBy
    ) public userExists(email) {
        _setStatus(email, UserStatus.Approved, reason, updatedBy);
    }

    // Function to get the current status of a user
    function getCurrentStatus(
        string memory email
    ) public view returns (UserStatus) {
        return userCurrentStatus[email];
    }

    // Function to get the status history of a user
    function getStatusHistory(
        string memory email
    ) public view returns (StatusHistory[] memory) {
        return userStatusHistory[email];
    }

    // Function to update user address
    function updateAddress(
        string memory email,
        string memory newAddress
    ) public userExists(email) {
        userCurrentAddress[email] = newAddress;
    }

    // Function to get the current address of a user
    function getCurrentAddress(
        string memory email
    ) public view returns (string memory) {
        return userCurrentAddress[email];
    }

    // Function to update user profile picture
    function updateProfilePic(
        string memory email,
        string memory filename
    ) public userExists(email) {
        userProfilePic[email] = filename;
    }

    // Function to get the profile picture of a user
    function getProfilePic(
        string memory email
    ) public view returns (string memory) {
        return userProfilePic[email];
    }

    // Internal function to update user credits
    function _updateCredits(
        string memory email,
        int256 credits,
        string memory txnComment,
        string memory updatedBy
    ) internal userExists(email) isOrganizationOrAdmin(email) {
        int256 previousBalance = userCurrentCredits[email];
        userCurrentCredits[email] += credits;
        // Log credits change in history
        userCreditHistory[email].push(
            CreditHistory({
                previousBalance: previousBalance,
                creditChange: credits,
                newBalance: userCurrentCredits[email],
                txnComment: txnComment,
                updatedBy: updatedBy,
                updateTimestamp: block.timestamp
            })
        );

        // Emit event
        emit CreditsUpdated(
            email,
            previousBalance,
            userCurrentCredits[email],
            txnComment,
            block.timestamp,
            updatedBy
        );
    }

    // Function to update user credits
    function updateCredits(
        string memory email,
        int256 credits,
        string memory txnComment,
        string memory updatedBy
    ) public userExists(email) isOrganizationOrAdmin(email) {
        _updateCredits(email, credits, txnComment, updatedBy);
    }

    // Function to get the current credits of a user
    function getUserCredits(string memory email) public view returns (int256) {
        return userCurrentCredits[email];
    }

    // Function to get the credit history of a user
    function getCreditHistory(
        string memory email
    ) public view returns (CreditHistory[] memory) {
        return userCreditHistory[email];
    }

    // Getter function to retrieve user type
    function getUserType(string memory email) public view returns (UserType) {
        return userDetails[email].userType;
    }
}
