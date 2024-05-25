// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./UserManagement.sol";
import "./DocumentsManagement.sol";
import "./EmploymentManagement.sol";
import "./SkillsManagement.sol";

contract EmployeeManagement {
    struct access_keys {
        bool isActive;
        string lastUsedBy;
    }

    mapping(string => mapping(string => access_keys)) public employeeAccessKeys; // email => (accessKey => access_keys)
    mapping(string => string[]) public employeeAccessKeysList;

    UserManagement userManagement;
    DocumentsManagement documentsManagement;
    EmploymentManagement employmentManagement;
    SkillsManagement skillsManagement;

    constructor(address userManagementAddress, address documentsManagementAddress, address employmentManagementAddress, address skillsManagementAddress){
        userManagement = UserManagement(userManagementAddress);
        documentsManagement = DocumentsManagement(documentsManagementAddress);
        employmentManagement = EmploymentManagement(employmentManagementAddress);
        skillsManagement = SkillsManagement(skillsManagementAddress);
    }

    modifier isEmployee(string memory email) {
        require(
            userManagement.getUserType(email) ==
                UserManagement.UserType.Employee,
            "Unauthorized"
        );
        _;
    }

    struct EmployeeProfile {
        UserManagement.User User;
        DocumentsManagement.EmployeeDocument[] Documents;
        EmploymentManagement.EmploymentDetails EmployementCurrent;
        EmploymentManagement.EmploymentHistory[] EmployementHistory;
        SkillsManagement.AllSkillsResponse[]        EmployeeSkills;
    }
    
    function getEmployeeProfile(
        string memory email
    ) public isEmployee(email) view returns (EmployeeProfile memory) {
        UserManagement.User memory user = userManagement.getUser(email);
        DocumentsManagement.EmployeeDocument[] memory documents = documentsManagement.getAllDocuments(email);
        EmploymentManagement.EmploymentDetails memory employmentCurrent = employmentManagement.getCurrentEmployment(email);
        EmploymentManagement.EmploymentHistory[] memory employmentHistory = employmentManagement.getEmploymentHistory(email);
        SkillsManagement.AllSkillsResponse[] memory employeeSkills = skillsManagement.getSkills(email);
        return EmployeeProfile(
            user,
            documents,
            employmentCurrent,
            employmentHistory,
            employeeSkills
        );
    }

    function addAccessKey(string memory email) public isEmployee(email) {
        // generate random 8-10 digit string
        bytes32 accessKey = keccak256(
            abi.encodePacked(block.timestamp, block.difficulty, email)
        );
        string memory accessKeyStr = _bytes32ToString(accessKey);

        access_keys memory newAccessKey = access_keys(true, "");

        employeeAccessKeys[email][accessKeyStr] = newAccessKey;
        employeeAccessKeysList[email].push(accessKeyStr);
    }

    function disableAccessKey(
        string memory email,
        string memory accessKey
    ) public isEmployee(email) {
        require(
            employeeAccessKeys[email][accessKey].isActive,
            "Access key is not active"
        );
        employeeAccessKeys[email][accessKey].isActive = false;
    }

    function AccessKeyIsActive(
        string memory email,
        string memory accessKey,
        string memory used_by
    ) public isEmployee(email) returns (bool) {
        require(
            employeeAccessKeys[email][accessKey].isActive,
            "Access key is not active"
        );
        employeeAccessKeys[email][accessKey].lastUsedBy = used_by;
        return employeeAccessKeys[email][accessKey].isActive;
    }

    function _bytes32ToString(
        bytes32 _bytes32
    ) private pure returns (string memory) {
        uint8 i = 0;
        while (i < 32 && _bytes32[i] != 0) {
            i++;
        }
        bytes memory bytesArray = new bytes(i);
        for (i = 0; i < 32 && _bytes32[i] != 0; i++) {
            bytesArray[i] = _bytes32[i];
        }
        return string(bytesArray);
    }
}
