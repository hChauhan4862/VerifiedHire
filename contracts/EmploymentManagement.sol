// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./UserManagement.sol";

contract EmploymentManagement {
    enum Employment_Status {
        Joined,
        Promoted,
        Resigned,
        Retired
    }
    struct EmploymentDetails {
        string organization;
        uint256 startDate;
        uint256 endDate;
        string position;
        bool active;
    }

    struct EmploymentHistory {
        string organization;
        uint256 actdate;
        string position;
        Employment_Status status;
        string comments;
        bool isVerified;
    }

    mapping(string => EmploymentDetails) public currentEmployment;
    mapping(string => EmploymentHistory[]) public employmentHistories;
    
    event EmploymentEvent(
        string email,
        string organization,
        string position,
        Employment_Status status,
        uint256 date
    );

    UserManagement userManagement;

    constructor(address userManagementAddress) {
        userManagement = UserManagement(userManagementAddress);
    }

    modifier isEmployee(string memory email) {
        require(
            userManagement.getUserType(email) == UserManagement.UserType.Employee,
            "Unauthorized"
        );
        _;
    }

    function joinCompany(
        string memory email,
        string memory organization,
        string memory position,
        uint256 startDate,
        string memory comments,
        bool isVerified
    ) public isEmployee(email) {
        // require(
        //     !currentEmployment[email].active,
        //     "Employee is already employed"
        // );

        currentEmployment[email] = EmploymentDetails({
            organization: organization,
            startDate: startDate,
            endDate: 0,
            position: position,
            active: true
        });

        employmentHistories[email].push(
            EmploymentHistory({
                organization: organization,
                actdate: startDate,
                position: position,
                status: Employment_Status.Joined,
                comments: comments,
                isVerified: isVerified
            })
        );

        emit EmploymentEvent(
            email,
            organization,
            position,
            Employment_Status.Joined,
            startDate
        );
    }

    function promoteEmployee(
        string memory email,
        string memory organization,
        string memory newPosition,
        uint256 date,
        string memory comments,
        bool isVerified
    ) public isEmployee(email) {
        EmploymentDetails storage details = currentEmployment[email];

        employmentHistories[email].push(
            EmploymentHistory({
                organization: organization,
                actdate: date,
                position: newPosition,
                status: Employment_Status.Promoted,
                comments: comments,
                isVerified: isVerified
            })
        );

        details.organization = organization;
        details.position = newPosition;
        details.startDate = date;

        emit EmploymentEvent(
            email,
            details.organization,
            newPosition,
            Employment_Status.Promoted,
            date
        );
    }

    function endEmployment(
        string memory email,
        string memory organization,
        uint256 date,
        Employment_Status status,
        string memory comments,
        bool isVerified
    ) public isEmployee(email) {
        EmploymentDetails storage details = currentEmployment[email];
        details.organization = organization;
        details.endDate = date;
        details.active = false;

        employmentHistories[email].push(
            EmploymentHistory({
                organization: details.organization,
                actdate: date,
                position: details.position,
                status: status,
                comments: comments,
                isVerified: isVerified
            })
        );

        emit EmploymentEvent(
            email,
            details.organization,
            details.position,
            status,
            date
        );
    }

    function getCurrentEmployment(
        string memory email
    ) public view returns (EmploymentDetails memory) {
        return currentEmployment[email];
    }

    function getEmploymentHistory(
        string memory email
    ) public view returns (EmploymentHistory[] memory) {
        return employmentHistories[email];
    }
}