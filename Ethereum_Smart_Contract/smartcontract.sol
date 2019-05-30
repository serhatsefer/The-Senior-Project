pragma solidity ^0.4.22;

contract SimpleBank {
    uint8 private clientCount;
    mapping (address => uint) private balances;
    address _seller;
    address public owner;
    bool complete;

    constructor() public payable {
    
        /* Set the owner to the creator of this contract */
        owner = msg.sender;
        clientCount = 0;
    }
	
    function confirm() public returns (uint) {
       
       
       /* if (clientCount < 3) {
            clientCount++;
            balances[msg.sender] += 10 ether;
        }
        */
        if(msg.sender != owner){
        //balances[owner] += balances[msg.sender];
        balances[_seller] += balances[msg.sender];
        
        balances[msg.sender] = 0;
            
        }
        
        return balances[msg.sender];
    }


    function pay(address seller) public payable returns (uint) {
        balances[msg.sender] += msg.value;
        _seller = seller;
        emit LogDepositMade(msg.sender, msg.value);
        return balances[msg.sender];
    }


    function withdraw(uint withdrawAmount) public returns (uint remainingBal) {
        // Check enough balance available, otherwise just return balance
        if (withdrawAmount <= balances[msg.sender]) {
            balances[msg.sender] -= withdrawAmount;
            msg.sender.transfer(withdrawAmount);
        }
        return balances[msg.sender];
    }


   function yourbalance() public constant returns (uint) {
        return balances[msg.sender];
    }

    function total() public constant returns (uint) {
        return address(this).balance;
    }
    
   
}
