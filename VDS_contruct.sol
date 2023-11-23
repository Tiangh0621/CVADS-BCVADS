pragma solidity >=0.6.12 <0.9.0;

contract VDS {
  /**
   * @dev Prints Hello World string
   */
  bytes10 dieta;
  uint public count = 0;
  address public owner;
    constructor(bytes10 dieta_jian)  {
        owner = msg.sender;
        dieta = dieta_jian;
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
    // 0 represent error, 1 represent right, 2 represent abstain  
  }
  mapping(address => para) public  server;
  mapping (uint => address) private ser_list;
  function Init(bytes10 sigma) payable  public{
      server[msg.sender].balances = msg.value;
      server[msg.sender].sigma = sigma;
      server[msg.sender].id = count;
      ser_list[count] = msg.sender;
      count ++;
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
  function audit_chal() public  {
    if (msg.sender == owner){
      uint z = random();
      uint r1 = random()/2;
      uint r2 = random()/4;
      chal.z = z;
      chal.r1 = r1;
      chal.r2 = r2;
    }
  }
  mapping (address => audit_proof) public  server_audit_proof;
  function audit_response(bytes10 rou) public {
    server_audit_proof[msg.sender].proof = rou;
  }
  function audit_result(address auditee, bool if_valid) public {
    server_audit_proof[auditee].result[msg.sender] = if_valid;

  }
  function audit_judge(address server_id) public returns(bool) {
    uint i;
    bool res1;
    bool res2;
    res1 = server_audit_proof[server_id].result[ser_list[0]];
    for(i=1; i<count; i++){
      res2 = server_audit_proof[server_id].result[ser_list[i]];
      if(res1 != res2){
        server_audit_proof[server_id].if_abstain = true;
        return false;
      }
    }
    if (res2 == false){
      server[server_id].balances = 0;
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
      for(uint i =0;i<count;i++){
        if(ser_list[i] != fault_point){
          server[ser_list[i]].balances += ballots_ser/(count-1); 
        }
      }
      return true;
    }
    return  false;
  }
  function update(bytes10 daita_jian) public {
    if (msg.sender == owner){
      dieta = daita_jian;
    }
  }

}
 