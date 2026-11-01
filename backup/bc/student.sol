// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * ============================================================================
 * Lab Practice - III (LP-III) | BE Computer Engineering (SPPU 2019 Pattern)
 * Group C - Assignment No: 4 (BT4)
 * Title: Write a program in Solidity to create Student data. Use the following
 *        constructs:
 *        1. Structures (struct Student)
 *        2. Arrays (Dynamic array & Fixed array)
 *        3. Fallback (receive() and fallback() functions)
 *        Deploy this as a smart contract on Ethereum and observe the 
 *        transaction fee and gas values.
 * Reference: Lab Manual Pages 155-162
 * ============================================================================
 * 
 * INSTRUCTIONS FOR REMIX IDE DEPLOYMENT & TESTING (https://remix.ethereum.org):
 * 1. Open Remix IDE -> Create file 'student.sol' in 'contracts/'.
 * 2. In Solidity Compiler tab -> Select version 0.8.20+ -> Click 'Compile student.sol'.
 * 3. In Deploy & Run tab -> Select 'Remix VM (London)' -> Click 'Deploy'.
 * 4. Expand deployed contract under 'Deployed Contracts':
 *    - Add Student: Call 'addStudent' with _rollNo = 1, _name = "Alice", _marks = 92.
 *    - Read Student: Call 'getStudentByIndex' with _index = 0, or 'getStudentByRollNo' with _rollNo = 1.
 *    - Top Rankers (Fixed Array): Call 'setTopRankers' with r1 = 1, r2 = 2, r3 = 3.
 *    - Check Array Length: Call 'getStudentCount' -> returns total registered students.
 *    - Test Fallback/Receive: Under 'Low level interactions' at bottom of contract panel,
 *      enter 1 in 'CALLDATA' and click 'Transact' to trigger fallback().
 * ============================================================================
 */

contract StudentDataManagement {

    // ------------------------------------------------------------------------
    // Construct 1: Structure (struct Student)
    // ------------------------------------------------------------------------
    struct Student {
        uint256 rollNo;      // Unique Student Roll Number
        string name;         // Student Full Name
        uint256 marks;       // Examination Marks / Percentage
        bool isEnrolled;     // Enrollment status
    }

    // ------------------------------------------------------------------------
    // Construct 2: Array Declarations
    // ------------------------------------------------------------------------
    // Dynamic Array of Structs: Dynamically expands as new students are added
    Student[] public studentList;

    // Fixed-Size Array: Stores exactly 3 top ranker roll numbers
    uint256[3] public topRankersRollNo;

    // Mapping for fast existence lookup to prevent duplicate roll numbers
    mapping(uint256 => bool) private rollExists;

    // Mapping roll number to array index
    mapping(uint256 => uint256) private rollToIndex;

    // ------------------------------------------------------------------------
    // Events (Logged permanently in Ethereum transaction receipts)
    // ------------------------------------------------------------------------
    event StudentAdded(uint256 indexed rollNo, string name, uint256 marks);
    event StudentUpdated(uint256 indexed rollNo, uint256 newMarks);
    event FallbackTriggered(address indexed sender, uint256 amount, bytes data);
    event EtherReceived(address indexed sender, uint256 amount);

    /**
     * @notice Add a new student record to the dynamic array.
     * @param _rollNo Unique roll number for the student.
     * @param _name Name of the student.
     * @param _marks Marks obtained.
     */
    function addStudent(
        uint256 _rollNo,
        string memory _name,
        uint256 _marks
    ) public {
        require(!rollExists[_rollNo], "Error: Student with this Roll Number already exists.");
        require(_rollNo > 0, "Error: Invalid Roll Number.");
        require(bytes(_name).length > 0, "Error: Student name cannot be empty.");

        // Construct and push new Student struct to dynamic array
        studentList.push(Student({
            rollNo: _rollNo,
            name: _name,
            marks: _marks,
            isEnrolled: true
        }));

        rollExists[_rollNo] = true;
        rollToIndex[_rollNo] = studentList.length - 1;

        emit StudentAdded(_rollNo, _name, _marks);
    }

    /**
     * @notice Get total count of registered students in the dynamic array.
     * @return Total number of students.
     */
    function getStudentCount() public view returns (uint256) {
        return studentList.length;
    }

    /**
     * @notice Get student details by dynamic array index position.
     * @param _index Index in the studentList array (0-indexed).
     */
    function getStudentByIndex(uint256 _index) public view returns (
        uint256 rollNo,
        string memory name,
        uint256 marks,
        bool isEnrolled
    ) {
        require(_index < studentList.length, "Error: Index out of bounds.");
        Student memory s = studentList[_index];
        return (s.rollNo, s.name, s.marks, s.isEnrolled);
    }

    /**
     * @notice Query student record directly by Roll Number.
     * @param _rollNo Student Roll Number to search.
     */
    function getStudentByRollNo(uint256 _rollNo) public view returns (
        uint256 rollNo,
        string memory name,
        uint256 marks,
        bool isEnrolled
    ) {
        require(rollExists[_rollNo], "Error: Student Roll Number not found.");
        uint256 index = rollToIndex[_rollNo];
        Student memory s = studentList[index];
        return (s.rollNo, s.name, s.marks, s.isEnrolled);
    }

    /**
     * @notice Update marks for an existing student record.
     * @param _rollNo Student Roll Number.
     * @param _newMarks Updated marks.
     */
    function updateMarks(uint256 _rollNo, uint256 _newMarks) public {
        require(rollExists[_rollNo], "Error: Student Roll Number not found.");
        uint256 index = rollToIndex[_rollNo];
        studentList[index].marks = _newMarks;

        emit StudentUpdated(_rollNo, _newMarks);
    }

    /**
     * @notice Set top 3 ranker roll numbers in the fixed-size array.
     * @param r1 Roll number of 1st ranker.
     * @param r2 Roll number of 2nd ranker.
     * @param r3 Roll number of 3rd ranker.
     */
    function setTopRankers(uint256 r1, uint256 r2, uint256 r3) public {
        topRankersRollNo[0] = r1;
        topRankersRollNo[1] = r2;
        topRankersRollNo[2] = r3;
    }

    /**
     * @notice View the top 3 rankers from the fixed-size array.
     */
    function getTopRankers() public view returns (uint256[3] memory) {
        return topRankersRollNo;
    }

    // ------------------------------------------------------------------------
    // Construct 3: Fallback & Receive Functions
    // ------------------------------------------------------------------------
    /**
     * @notice Receive function: Executed automatically on plain ETH transfers (empty calldata).
     */
    receive() external payable {
        emit EtherReceived(msg.sender, msg.value);
    }

    /**
     * @notice Fallback function: Executed when calling invalid non-existent functions or sending data.
     */
    fallback() external payable {
        emit FallbackTriggered(msg.sender, msg.value, msg.data);
    }
}
