// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * ============================================================================
 * Lab Practice - III (LP-III) | BE Computer Engineering (SPPU 2019 Pattern)
 * Group C - Assignment No: 3 (BT3)
 * Title: Write a smart contract on a test network, for Bank account of a 
 *        customer for following operations:
 *        1. Deposit money
 *        2. Withdraw money
 *        3. Show balance
 * Reference: Lab Manual Pages 138-154
 * ============================================================================
 * 
 * INSTRUCTIONS FOR REMIX IDE DEPLOYMENT & TESTING (https://remix.ethereum.org):
 * 1. Open Remix IDE in browser -> Create file 'bank.sol' inside 'contracts/'.
 * 2. In Solidity Compiler tab -> Select 0.8.20+ -> Click 'Compile bank.sol'.
 * 3. In Deploy & Run tab -> Select 'Remix VM (London)' or 'Injected Provider - MetaMask'.
 * 4. Click 'Deploy'.
 * 5. Expand deployed contract:
 *    - Deposit: In 'Value' box enter 5, select 'Ether', click 'deposit'.
 *    - Check Balance: Click 'getBalance' to see your account balance in Wei.
 *    - Withdraw: In 'withdraw' box enter amount in Wei (or use ether units), click 'withdraw'.
 *    - Total Contract Balance: Click 'getContractTotalBalance' (Owner only).
 * ============================================================================
 */

contract SimpleBank {

    // 1. State Variables (Permanently stored on the Ethereum blockchain)
    address public owner;
    mapping(address => uint256) private balances;

    // 2. Events (Logged in transaction receipts for dApps / frontends)
    event DepositMade(address indexed accountAddress, uint256 amount);
    event WithdrawalMade(address indexed accountAddress, uint256 amount);
    event FallbackReceived(address indexed sender, uint256 amount, bytes data);

    // 3. Modifiers (Access control checks)
    modifier onlyOwner() {
        require(msg.sender == owner, "Error: Only the contract owner can call this function.");
        _;
    }

    // 4. Constructor (Executes once upon contract deployment)
    constructor() {
        owner = msg.sender; // Set deploying account as bank administrator
    }

    /**
     * @notice Deposit Ether into the caller's bank account.
     * @dev Function must be marked 'payable' to receive native ETH with msg.value.
     * @return New balance of the calling user in Wei.
     */
    function deposit() public payable returns (uint256) {
        require(msg.value > 0, "Error: Deposit amount must be greater than 0 Wei.");

        // Credit caller's account balance
        balances[msg.sender] += msg.value;

        // Emit event into Ethereum receipt log
        emit DepositMade(msg.sender, msg.value);

        return balances[msg.sender];
    }

    /**
     * @notice Withdraw Ether from the caller's bank balance.
     * @dev Follows Checks-Effects-Interactions pattern to prevent Reentrancy attacks.
     * @param withdrawAmount The amount in Wei to withdraw.
     * @return Remaining balance of the calling user.
     */
    function withdraw(uint256 withdrawAmount) public returns (uint256) {
        require(withdrawAmount > 0, "Error: Withdrawal amount must be greater than 0.");
        require(balances[msg.sender] >= withdrawAmount, "Error: Insufficient account balance.");

        // EFFECT: Deduct balance BEFORE transferring funds to prevent reentrancy
        balances[msg.sender] -= withdrawAmount;

        // INTERACTION: Transfer funds securely using call{value: ...}
        (bool success, ) = payable(msg.sender).call{value: withdrawAmount}("");
        require(success, "Error: Failed to transfer Ether to caller.");

        // Emit logging event
        emit WithdrawalMade(msg.sender, withdrawAmount);

        return balances[msg.sender];
    }

    /**
     * @notice Check the deposited balance of the caller.
     * @dev 'view' function reads state without writing; incurs 0 Gas on off-chain read calls.
     * @return Balance in Wei.
     */
    function getBalance() public view returns (uint256) {
        return balances[msg.sender];
    }

    /**
     * @notice Check total balance held inside the contract vault.
     * @dev Restricted to contract owner / manager.
     * @return Total contract balance in Wei.
     */
    function getContractTotalBalance() public view onlyOwner returns (uint256) {
        return address(this).balance;
    }

    /**
     * @notice Receive function: Triggered automatically on plain ETH transfers (empty calldata).
     */
    receive() external payable {
        deposit();
    }

    /**
     * @notice Fallback function: Executed if no function signature matches the call.
     */
    fallback() external payable {
        emit FallbackReceived(msg.sender, msg.value, msg.data);
    }
}
