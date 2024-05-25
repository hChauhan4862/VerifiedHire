const UserManagement = artifacts.require("UserManagement");
const EmploymentManagement = artifacts.require("EmploymentManagement");
const DocumentsManagement = artifacts.require("DocumentsManagement");
const SkillsManagement = artifacts.require("SkillsManagement");
const EmployeeManagement = artifacts.require("EmployeeManagement");
const adminManagement = artifacts.require("AdminManagement")
const VerifiedHire = artifacts.require("VerifiedHire");

module.exports = async function (deployer) {
  await deployer.deploy(UserManagement);
  const userManagement = await UserManagement.deployed();

  await deployer.deploy(EmploymentManagement, userManagement.address); // Assuming it takes userManagement's address
  const employmentManagement = await EmploymentManagement.deployed();

  await deployer.deploy(DocumentsManagement, userManagement.address); // Assuming it takes userManagement's address
  const documentsManagement = await DocumentsManagement.deployed();

  await deployer.deploy(SkillsManagement, userManagement.address); // Assuming it takes userManagement's address
  const skillsManagement = await SkillsManagement.deployed();

  await deployer.deploy(EmployeeManagement, userManagement.address, documentsManagement.address, employmentManagement.address, skillsManagement.address); // Assuming it takes userManagement's address
  const employeeManagement = await EmployeeManagement.deployed();

  await deployer.deploy(adminManagement, userManagement.address); // Assuming it takes userManagement's address
  const admin = await adminManagement.deployed();

  await deployer.deploy(VerifiedHire, userManagement.address, employmentManagement.address, documentsManagement.address, skillsManagement.address, employeeManagement.address, adminManagement.address);
  const verifiedHire = await VerifiedHire.deployed();

  console.log("VerifiedHire deployed at:", verifiedHire.address);
};