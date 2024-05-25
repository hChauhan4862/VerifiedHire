
UserManagement Functions
	1.	registerUser
	•	Arguments: string memory name, string memory email, UserManagement.Gender gender, string memory phone, UserManagement.UserType userType, string memory password
	2.	doesUserExist
	•	Arguments: string memory email
	3.	listAllUsers
	•	Arguments: None
	4.	getAdminProfile
	•	Arguments: string memory email
	5.	login
	•	Arguments: string memory email, string memory password, string memory session_id, UserManagement.UserType userType
	6.	logout
	•	Arguments: string memory session_id
	7.	isSessionActive
	•	Arguments: string memory session_id
	8.	sessionData
	•	Arguments: string memory session_id
	9.	updateUserDetails
	•	Arguments: string memory email, string memory name, UserManagement.Gender gender, string memory phone, UserManagement.UserType userType
	10.	changePassword
	•	Arguments: string memory email, string memory newPassword
	11.	deactivateUser
	•	Arguments: string memory email, string memory reason, string memory updatedBy
	12.	activateUser
	•	Arguments: string memory email, string memory reason, string memory updatedBy
	13.	getCurrentStatus
	•	Arguments: string memory email
	14.	getStatusHistory
	•	Arguments: string memory email
	15.	updateAddress
	•	Arguments: string memory email, string memory newAddress
	16.	getCurrentAddress
	•	Arguments: string memory email
	17.	updateProfilePic
	•	Arguments: string memory email, string memory filename
	18.	getProfilePic
	•	Arguments: string memory email
	19.	updateCredits
	•	Arguments: string memory email, int256 credits, string memory txnComment, string memory updatedBy
	20.	getUserCredits
	•	Arguments: string memory email
	21.	getUserCreditsHistory
	•	Arguments: string memory email
	22.	getUserType
	•	Arguments: string memory email

EmploymentManagement Functions

	1.	joinCompany
	•	Arguments: string memory email, string memory organization, string memory position, uint256 startDate, string memory comments, bool isVerified
	2.	promoteEmployee
	•	Arguments: string memory email, string memory organization, string memory newPosition, uint256 date, string memory comments, bool isVerified
	3.	endEmployment
	•	Arguments: string memory email, string memory organization, uint256 date, EmploymentManagement.Employment_Status status, string memory comments, bool isVerified
	4.	getCurrentEmployment
	•	Arguments: string memory email
	5.	getEmploymentHistory
	•	Arguments: string memory email

DocumentsManagement Functions

	1.	addDocument
	•	Arguments: string memory email, DocumentsManagement.DocumentTypes documentType, string memory title, string memory document_id, string memory file_name, string memory file_url, string memory json_data, string memory verified_by, uint256 date
	2.	verifyDocument
	•	Arguments: string memory email, string memory documentHash, string memory verified_by
	3.	getDocument
	•	Arguments: string memory email, string memory documentHash
	4.	getDocumentHashes
	•	Arguments: string memory email
	5.	getAllDocuments
	•	Arguments: string memory email

SkillsManagement Functions

	1.	addSkill
	•	Arguments: string memory email, string memory skill, int score, string memory verified_by, uint256 date
	2.	getSkillScore
	•	Arguments: string memory email, string memory skill
	3.	getSkills
	•	Arguments: string memory email

EmployeeManagement Functions

	1.	addAccessKey
	•	Arguments: string memory email
	2.	disableAccessKey
	•	Arguments: string memory email, string memory accessKey