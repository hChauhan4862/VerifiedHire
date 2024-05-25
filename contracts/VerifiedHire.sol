// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./UserManagement.sol";
import "./EmploymentManagement.sol";
import "./DocumentsManagement.sol";
import "./SkillsManagement.sol";
import "./EmployeeManagement.sol";
import "./AdminManagement.sol";

contract VerifiedHire {
    UserManagement public userManagement;
    EmploymentManagement public employmentManagement;
    DocumentsManagement public documentsManagement;
    SkillsManagement public skillsManagement;
    EmployeeManagement public employeeManagement;
    AdminManagement public adminManagement;

    constructor(
        address userManagementAddress,
        address employmentManagementAddress,
        address documentsManagementAddress,
        address skillsManagementAddress,
        address employeeManagementAddress,
        address adminManagementAddress
    ) {
        userManagement = UserManagement(userManagementAddress);
        employmentManagement = EmploymentManagement(
            employmentManagementAddress
        );
        documentsManagement = DocumentsManagement(documentsManagementAddress);
        skillsManagement = SkillsManagement(skillsManagementAddress);
        employeeManagement = EmployeeManagement(employeeManagementAddress);
        adminManagement = AdminManagement(adminManagementAddress);
    }

    // UserManagement functions
    function registerUser(
        string memory name,
        string memory email,
        UserManagement.Gender gender,
        string memory phone,
        UserManagement.UserType userType,
        string memory password
    ) public {
        userManagement.registerUser(
            name,
            email,
            gender,
            phone,
            userType,
            password
        );
    }

    function doesUserExist(string memory email) public view returns (bool) {
        return userManagement.doesUserExist(email);
    }

    function listAllUsers() public view returns (UserManagement.User[] memory) {
        return userManagement.listAllUsers();
    }

    function getAdminProfile(
        string memory email
    ) public view returns (AdminManagement.AdminProfile memory) {
        return adminManagement.getAdminProfile(email);
    }

    function getOrganizationProfile(
        string memory email
    ) public view returns (UserManagement.Profile memory) {
        return userManagement.getUserProfile(email);
    }

    function getEmployeeProfile(
        string memory email
    ) public view returns (EmployeeManagement.EmployeeProfile memory) {
        return employeeManagement.getEmployeeProfile(email);
    }

    function login(
        string memory email,
        string memory password,
        string memory session_id,
        UserManagement.UserType userType
    ) public returns (bool) {
        return userManagement.login(email, password, session_id, userType);
    }

    function logout(string memory session_id) public {
        userManagement.logout(session_id);
    }

    function isSessionActive(
        string memory session_id
    ) public view returns (bool) {
        return userManagement.isSessionActive(session_id);
    }

    function sessionData(
        string memory session_id
    ) public view returns (string memory) {
        return userManagement.sessionData(session_id);
    }

    function updateUserDetails(
        string memory email,
        string memory name,
        UserManagement.Gender gender,
        string memory phone,
        UserManagement.UserType userType
    ) public {
        userManagement.updateUserDetails(email, name, gender, phone, userType);
    }

    function changePassword(
        string memory email,
        string memory newPassword
    ) public {
        userManagement.changePassword(email, newPassword);
    }

    function deactivateUser(
        string memory email,
        string memory reason,
        string memory updatedBy
    ) public {
        userManagement.deactivateUser(email, reason, updatedBy);
    }

    function activateUser(
        string memory email,
        string memory reason,
        string memory updatedBy
    ) public {
        userManagement.activateUser(email, reason, updatedBy);
    }

    function getCurrentStatus(
        string memory email
    ) public view returns (UserManagement.UserStatus) {
        return userManagement.getCurrentStatus(email);
    }

    function getStatusHistory(
        string memory email
    ) public view returns (UserManagement.StatusHistory[] memory) {
        return userManagement.getStatusHistory(email);
    }

    function updateAddress(
        string memory email,
        string memory newAddress
    ) public {
        userManagement.updateAddress(email, newAddress);
    }

    function getCurrentAddress(
        string memory email
    ) public view returns (string memory) {
        return userManagement.getCurrentAddress(email);
    }

    function updateProfilePic(
        string memory email,
        string memory filename
    ) public {
        userManagement.updateProfilePic(email, filename);
    }

    function getProfilePic(
        string memory email
    ) public view returns (string memory) {
        return userManagement.getProfilePic(email);
    }

    function updateCredits(
        string memory email,
        int256 credits,
        string memory txnComment,
        string memory updatedBy
    ) public {
        userManagement.updateCredits(email, credits, txnComment, updatedBy);
    }

    function getUserCredits(string memory email) public view returns (int256) {
        return userManagement.getUserCredits(email);
    }

    function getUserCreditsHistory(
        string memory email
    ) public view returns (UserManagement.CreditHistory[] memory) {
        return userManagement.getCreditHistory(email);
    }

    function getUserType(
        string memory email
    ) public view returns (UserManagement.UserType) {
        return userManagement.getUserType(email);
    }

    // EmploymentManagement functions
    function joinCompany(
        string memory email,
        string memory organization,
        string memory position,
        uint256 startDate,
        string memory comments,
        bool isVerified
    ) public {
        employmentManagement.joinCompany(
            email,
            organization,
            position,
            startDate,
            comments,
            isVerified
        );
    }

    function promoteEmployee(
        string memory email,
        string memory organization,
        string memory newPosition,
        uint256 date,
        string memory comments,
        bool isVerified
    ) public {
        employmentManagement.promoteEmployee(
            email,
            organization,
            newPosition,
            date,
            comments,
            isVerified
        );
    }

    function endEmployment(
        string memory email,
        string memory organization,
        uint256 date,
        EmploymentManagement.Employment_Status status,
        string memory comments,
        bool isVerified
    ) public {
        employmentManagement.endEmployment(
            email,
            organization,
            date,
            status,
            comments,
            isVerified
        );
    }

    function getCurrentEmployment(
        string memory email
    ) public view returns (EmploymentManagement.EmploymentDetails memory) {
        return employmentManagement.getCurrentEmployment(email);
    }

    function getEmploymentHistory(
        string memory email
    ) public view returns (EmploymentManagement.EmploymentHistory[] memory) {
        return employmentManagement.getEmploymentHistory(email);
    }

    // DocumentsManagement functions
    function addDocument(
        string memory email,
        DocumentsManagement.DocumentTypes documentType,
        string memory title,
        string memory document_id,
        string memory file_name,
        string memory file_url,
        string memory json_data,
        string memory verified_by,
        uint256 date
    ) public {
        documentsManagement.addDocument(
            email,
            documentType,
            title,
            document_id,
            file_name,
            file_url,
            json_data,
            verified_by,
            date
        );
    }

    function verifyDocument(
        string memory email,
        string memory documentHash,
        string memory verified_by
    ) public {
        documentsManagement.verifyDocument(email, documentHash, verified_by);
    }

    function getDocument(
        string memory email,
        string memory documentHash
    ) public view returns (DocumentsManagement.EmployeeDocument memory) {
        return documentsManagement.getDocument(email, documentHash);
    }

    function getDocumentHashes(
        string memory email
    ) public view returns (string[] memory) {
        return documentsManagement.getDocumentHashes(email);
    }

    function getAllDocuments(
        string memory email
    ) public view returns (DocumentsManagement.EmployeeDocument[] memory) {
        return documentsManagement.getAllDocuments(email);
    }

    // SkillsManagement functions
    function addSkill(
        string memory email,
        string memory skill,
        int score,
        string memory verified_by
    ) public {
        skillsManagement.addSkill(email, skill, score, verified_by); 
    }

    function getSkillScore(
        string memory email,
        string memory skill
    ) public view returns (int) {
        return skillsManagement.getSkillScore(email, skill);
    }

    function getSkills(
        string memory email
    ) public view returns (SkillsManagement.AllSkillsResponse[] memory) {
        return skillsManagement.getSkills(email);
    }

    // EmployeeManagement functions
    function addAccessKey(string memory email) public {
        employeeManagement.addAccessKey(email);
    }

    function AccessKeyIsActive(
        string memory email,
        string memory accessKey,
        string memory used_by
    ) public returns (bool) {
        return employeeManagement.AccessKeyIsActive(email, accessKey, used_by);
    }

    function disableAccessKey(
        string memory email,
        string memory accessKey
    ) public {
        employeeManagement.disableAccessKey(email, accessKey);
    }
}
