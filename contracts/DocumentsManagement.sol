// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./UserManagement.sol";

contract DocumentsManagement {
    enum DocumentTypes {
        Education,
        GovtID,
        Files
    }
    struct EmployeeDocument {
        string documentHash;
        DocumentTypes documentType;
        string title;
        string document_id;
        string file_name;
        string file_url;
        string json_data;
        string verified_by;
        bool isVerified;
        uint256 date;
    }

    mapping(string => mapping(string => EmployeeDocument)) public employeeDocuments; // email => (hash => EmployeeDocument)
    mapping(string => string[]) public employeeDocumentHashes; // email => [hashes]

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

   // Function to add a new document for an employee
    function addDocument(
        string memory email,
        DocumentTypes documentType,
        string memory title,
        string memory document_id,
        string memory file_name,
        string memory file_url,
        string memory json_data,
        string memory verified_by,
        uint256 date
    ) public isEmployee(email){
        // Generate the document hash
        bytes32 documentHash = keccak256(abi.encodePacked(
            email, documentType, title, document_id, file_name, file_url, json_data
        ));

        string memory documentHashStr = _bytes32ToString(documentHash);

        // Ensure the document does not already exist
        require(bytes(employeeDocuments[email][documentHashStr].documentHash).length == 0, "Document already exists");

        // Create the new document
        EmployeeDocument memory newDocument = EmployeeDocument({
            documentHash: documentHashStr,
            documentType: documentType,
            title: title,
            document_id: document_id,
            file_name: file_name,
            file_url: file_url,
            json_data: json_data,
            verified_by: verified_by,
            isVerified: (bytes(verified_by).length > 0), // If verified_by is not empty, the document is verified
            date: date
        });

        // Store the document
        employeeDocuments[email][documentHashStr] = newDocument;
        employeeDocumentHashes[email].push(documentHashStr);
    }

    function verifyDocument(string memory email, string memory documentHash, string memory verified_by) public {
        // Ensure the document exists
        require(bytes(employeeDocuments[email][documentHash].documentHash).length > 0, "Document does not exist");

        // Update the document
        employeeDocuments[email][documentHash].verified_by = verified_by;
        employeeDocuments[email][documentHash].isVerified = true;
    }

    // Function to get a document by email and hash
    function getDocument(string memory email, string memory documentHash) public view returns (EmployeeDocument memory) {
        return employeeDocuments[email][documentHash];
    }

    // Function to get all document hashes for an employee
    function getDocumentHashes(string memory email) public view returns (string[] memory) {
        return employeeDocumentHashes[email];
    }

    function getAllDocuments(string memory email) public view returns (EmployeeDocument[] memory){
        EmployeeDocument[] memory documents = new EmployeeDocument[](employeeDocumentHashes[email].length);
        for(uint i = 0; i < employeeDocumentHashes[email].length; i++){
            documents[i] = employeeDocuments[email][employeeDocumentHashes[email][i]];
        }
        return documents;
    }

    // Helper function to convert bytes32 to string
    function _bytes32ToString(bytes32 _bytes32) private pure returns (string memory) {
        uint8 i = 0;
        while(i < 32 && _bytes32[i] != 0) {
            i++;
        }
        bytes memory bytesArray = new bytes(i);
        for (i = 0; i < 32 && _bytes32[i] != 0; i++) {
            bytesArray[i] = _bytes32[i];
        }
        return string(bytesArray);
    }
}