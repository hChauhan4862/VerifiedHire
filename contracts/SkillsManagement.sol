// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./UserManagement.sol";

contract SkillsManagement {
    struct SkillsVotes {
        int score; // 0 - 10
        string verified_by;
        bool isVerified;
        uint256 date;
    }

    mapping(string => mapping(string => SkillsVotes[])) public employeeSkillsScore; // email => (skill => Votes[])
    mapping(string => string[]) public employeeSkills;

    UserManagement userManagement;

    constructor(address userManagementAddress) {
        userManagement = UserManagement(userManagementAddress);
    }

    modifier isEmployee(string memory email) {
        require(
            userManagement.getUserType(email) ==
                UserManagement.UserType.Employee,
            "Unauthorized"
        );
        _;
    }

    // Function to add a new Skill for an employee
    function addSkill(
        string memory email,
        string memory skill,
        int score,
        string memory verified_by
    ) public isEmployee(email) {
        bool skillExists = false;

        if (employeeSkillsScore[email][skill].length == 0 || keccak256(abi.encodePacked(verified_by)) == keccak256(abi.encodePacked("System"))) {
            employeeSkillsScore[email][skill].push(SkillsVotes({
                score: score,
                verified_by: verified_by,
                isVerified: true,
                date: block.timestamp
            }));
        } else {
            skillExists = false;
            bytes32 verifiedByHash = keccak256(abi.encodePacked(verified_by));
            for (uint256 i = 0; i < employeeSkillsScore[email][skill].length; i++) {
                if (keccak256(abi.encodePacked(employeeSkillsScore[email][skill][i].verified_by)) == verifiedByHash) {
                    skillExists = true;
                    break;
                }
            }
            if (!skillExists) {
                employeeSkillsScore[email][skill].push(SkillsVotes({
                    score: score,
                    verified_by: verified_by,
                    isVerified: true,
                    date: block.timestamp
                }));
            }
        }

        skillExists = false;
        bytes32 skillHash = keccak256(abi.encodePacked(skill));
        for (uint256 i = 0; i < employeeSkills[email].length; i++) {
            if (keccak256(abi.encodePacked(employeeSkills[email][i])) == skillHash) {
                skillExists = true;
                break;
            }
        }
        if (!skillExists) {
            employeeSkills[email].push(skill);
        }
    }

    // Function to get the average score of a skill
    function getSkillScore(string memory email, string memory skill) public view returns (int) {
        int totalScore = 0;
        int totalVotes = 0;
        for (uint256 i = 0; i < employeeSkillsScore[email][skill].length; i++) {
            if (employeeSkillsScore[email][skill][i].isVerified) {
                totalScore += employeeSkillsScore[email][skill][i].score;
                totalVotes++;
            }
        }
        if (totalVotes == 0) {
            return 0;
        }
        return totalScore / totalVotes;
    }

    struct AllSkillsResponse {
        string skill;
        int avgscore;
        SkillsVotes[] votes;
    }

    // Function to return all skills with average and their votes
    function getSkills(string memory email) public view returns (AllSkillsResponse[] memory) {
        AllSkillsResponse[] memory response = new AllSkillsResponse[](employeeSkills[email].length);
        for (uint256 i = 0; i < employeeSkills[email].length; i++) {
            response[i].skill = employeeSkills[email][i];
            response[i].avgscore = getSkillScore(email, employeeSkills[email][i]);
            response[i].votes = employeeSkillsScore[email][employeeSkills[email][i]];
        }
        return response;
    }
}