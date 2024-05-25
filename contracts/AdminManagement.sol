// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./UserManagement.sol";

contract AdminManagement {
    UserManagement public userManagement;
    
    struct AdminProfile {
        UserManagement.User User;
    }

    constructor(address userManagementAddress) {
        userManagement = UserManagement(userManagementAddress);
    }

    modifier isAdmin(string memory email) {
        require(
            userManagement.getUserType(email) == UserManagement.UserType.Admin,
            "Unauthorized"
        );
        _;
    }

    function getAdminProfile(
        string memory email
    ) public isAdmin(email) view returns (AdminProfile memory) {
        UserManagement.User memory user = userManagement.getUser(email);
        return AdminProfile(user);
    }

}