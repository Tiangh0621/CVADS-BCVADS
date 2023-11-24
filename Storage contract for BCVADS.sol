// SPDX-License-Identifier: MIT
pragma solidity >=0.6.12 <0.9.0;

contract VDS {
  /**
   * @dev Prints Hello World string
   */
  bytes10 delta;
  uint public server_num = 0;
  address public owner;
  uint reward;
  uint u_balance;
  bool alert;
  mapping (uint=>address) public  audit_server;
  uint max_auditor;
    constructor(bytes10 delta_jian, uint reward_in, uint auditor_num) payable  {
        owner = msg.sender;
        delta = delta_jian;
        reward = reward_in;
        u_balance = msg.value;
        max_auditor = auditor_num;
    }
  struct para {
    uint id;
    uint balances;
    bytes10 sigma;
    bytes10 rou;
  }
  struct audit_proof {
    bytes10 proof;
    mapping (address => bool) result;
    bool if_abstain;
  }
  mapping(address => para) public  server;
  mapping (uint => address) private ser_list;
  function Init(bytes10 sigma) payable  public{
      server[msg.sender].balances = msg.value;
      server[msg.sender].sigma = sigma;
      server[msg.sender].id = server_num;
      ser_list[server_num] = msg.sender;
      server_num ++;
  }
  function random() private view returns(uint) {
    return uint(keccak256(abi.encodePacked(block.timestamp,  
        msg.sender))) ;
  }
  struct CurrentChal {
    uint z ;
    uint r1 ;
    uint r2 ;
  }
  CurrentChal public  chal; 
  function audit_chal(address auditee) public  {
    if(alert){
      return ;
    } 
    if (msg.sender == owner){
      uint z = random();
      uint r1 = random()/2;
      uint r2 = random()/4;
      chal.z = z;
      chal.r1 = r1;
      chal.r2 = r2;
      uint k = z%server_num;
      for (uint i=0; i<max_auditor; i++){
        if (ser_list[(k+i)%server_num] != auditee){
          audit_server[i] = ser_list[(k+i)%server_num];
        }
        else {
          audit_server[i] = ser_list[(k-1)%server_num];
        }
      }
      
    }
  }
  function continue_AUDIT() payable  public {
    if (msg.sender == owner){
      u_balance += msg.value;
      if (u_balance >= reward*max_auditor){
        alert = false;
      }
    }
  }
  mapping (address => audit_proof) public  server_audit_proof;
  function audit_response(bytes10 rou) public {
    server_audit_proof[msg.sender].proof = rou;
  }
  uint audit_count = 0;
  function audit_result(address auditee, bool if_valid) public {
    server_audit_proof[auditee].result[msg.sender] = if_valid;
    audit_count ++;
    if (audit_count >= server_num-1){
      audit_judge(auditee);
    }

  }
  function audit_judge(address server_id) private  returns(bool) {
    uint i;
    bool res1;
    bool res2;
    res1 = server_audit_proof[server_id].result[ser_list[0]];
    for(i=1; i<max_auditor; i++){
      res2 = server_audit_proof[server_id].result[ser_list[i]];
      if(res1 != res2){
        server_audit_proof[server_id].if_abstain = true;
        return false;
      }
    }
    if (res2 == false){
      uint ballots_ser = server[server_id].balances;
      server[server_id].balances = 0;
      for(i =0;i<max_auditor;i++){
        if(audit_server[i] != server_id){
          server[ser_list[i]].balances += ballots_ser/(max_auditor); 
        }
      }

    }
    if (res2 == true){
      for(i =0;i<max_auditor;i++){
        server[audit_server[i]].balances += reward; 
        u_balance -= reward;
        if(u_balance <= reward*max_auditor){
          alert = true;
        }

      }

    }
    server_audit_proof[server_id] ;
    return true;
  }
  function user_judge(address server_id, address fault_point) public returns(bool){
    if (msg.sender == owner){
      if(server_audit_proof[server_id].if_abstain != true){
        return false;
      }
      uint ballots_ser;
      ballots_ser = server[fault_point].balances;
      server[fault_point].balances = 0;
      for(uint i =0;i<max_auditor;i++){
        if(audit_server[i] != fault_point){
          server[audit_server[i]].balances += ballots_ser/(max_auditor-1); 
        }
      }
      return true;
    }
    return  false;
  }
  function update(bytes10 delta_jian) public {
    if (msg.sender == owner){
      delta = delta_jian;
    }
  }

}
 