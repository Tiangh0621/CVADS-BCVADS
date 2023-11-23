# Tian_VDS
This project is an implementation of a paper about the VDS scheme.
## Code structure
To deploy this project, you should install a Python environment. Besides, you should compile VDS_constructor.sol first. We strongly recommend you use Remix first to test the sol code.
## For smart contract
For any data request, you should deploy one contract, in which all the participants can pre-pay a reward and deposit for further execution. 
## For other parts
We separate the function into different parts that are data_append, data_audit, data_update, and data_query. In each script, we accurately apply two classes, that are USER and SERVER or AUDITOR and AUDITEE, which can be easily applied in a real enviromment.
