import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {createClient,createAccount,generatePrivateKey} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {item,parts,before,after,missing} from '../src/fixture.js';
fs.mkdirSync('.private',{recursive:true});
const checkpoint='.private/live.json';
const s=fs.existsSync(checkpoint)?JSON.parse(fs.readFileSync(checkpoint)): {keys:[generatePrivateKey(),generatePrivateKey()],steps:{},id:'lamp-204'};
const accounts=s.keys.map(createAccount), clients=accounts.map(account=>createClient({chain:studionet,account}));
const owner=accounts[0].address.toLowerCase(),receiver=accounts[1].address.toLowerCase();
const source=fs.readFileSync('contracts/stillmark.py','utf8');
const evidence={protocol:'stillmark-1',network:61999,sourceSha256:createHash('sha256').update(source).digest('hex'),owner,receiver,id:s.id,fixture:'Authored lamp reports; two distinct zero-balance temporary test accounts controlled by one operator. Not independent people or a real physical inspection.'};
function save(){fs.writeFileSync(checkpoint,JSON.stringify(s));fs.writeFileSync('evidence/studionet.json',JSON.stringify({...evidence,address:s.address,steps:s.steps,records:s.records||[]},null,2));}
function good(tx){let r=tx.consensus_data?.leader_receipt;r=Array.isArray(r)?r.find(x=>x.mode==='leader'):r;return [7,'FINALIZED'].includes(tx.status)&&[6,'MAJORITY_AGREE'].includes(tx.result)&&r?.execution_result==='SUCCESS';}
async function step(label,who,method,args,expected=true){
 if(s.steps[label]?.done)return;
 let p=s.steps[label];
 if(!p){if(await clients[who].getChainId()!==61999)throw Error('WRONG_CHAIN');const gas=await clients[who].request({method:'eth_gasPrice',params:[]});if(BigInt(gas)!==0n)throw Error('NONZERO_GAS');
 s.steps[label]={sending:true,method,args,signer:accounts[who].address};save();
 const hash=method==='deploy'?await clients[who].deployContract({code:source,args:[],value:0n,leaderOnly:false}):await clients[who].writeContract({address:s.address,functionName:method,args,value:0n,leaderOnly:false});
 p=s.steps[label]={hash,method,args,signer:accounts[who].address};save();console.log(label,hash);}
 if(!p.hash)throw Error('Ambiguous send: inspect before retry');
 let tx;for(let i=0;i<12;i++){try{tx=await clients[0].waitForTransactionReceipt({hash:p.hash,status:'FINALIZED',interval:4000,retries:10,fullTransaction:true});break;}catch(e){console.log(label,'tracking',i,e.shortMessage||e.message);}}
 if(!tx)throw Error('Pending existing hash');p.receipt=tx;save();if(good(tx)!==expected)throw Error('Unexpected execution: '+label);
 if(method==='deploy'){s.address=tx.data?.contract_address||tx.contract_address;if(!s.address)throw Error('No address');if(await clients[0].getContractCode(s.address)!==source)throw Error('SOURCE_MISMATCH');}
 p.done=true;save();console.log(label,'verified');
}
async function read(id){return JSON.parse(await clients[0].readContract({address:s.address,functionName:'get_record',args:[owner,id],transactionHashVariant:'latest-final'}));}
await step('01-deploy',0,'deploy',[]);
await step('02-dispatch',0,'dispatch',[s.id,receiver,item,JSON.stringify(parts),before]);
await step('03-receive',1,'receive',[owner,s.id,after]);
await step('04-compare',0,'compare',[owner,s.id]);
let r=await read(s.id);if(r.result.findings.map(f=>f.label).join(',')!=='UNCHANGED,NEW_DAMAGE,UNCHANGED')throw Error('Unexpected comparison');
await step('05-stale-digest-denied',0,'acknowledge',[owner,s.id,'invalid-digest'],false);
await step('06-owner-acknowledges',0,'acknowledge',[owner,s.id,r.digest]);
await step('07-receiver-acknowledges',1,'acknowledge',[owner,s.id,r.digest]);
r=await read(s.id);if(r.status!=='ACKNOWLEDGED'||r.approvals.length!==2)throw Error('Missing bilateral acknowledgement');s.records=[r];save();
await step('08-incomplete-dispatch',0,'dispatch',['lamp-review',receiver,item,JSON.stringify(parts),before]);
await step('09-incomplete-receive',1,'receive',[owner,'lamp-review',missing]);
await step('10-incomplete-compare',1,'compare',[owner,'lamp-review']);
const review=await read('lamp-review');if(review.status!=='REVIEW')throw Error('Missing report did not block');s.records=[r,review];save();
await step('11-review-ack-denied',0,'acknowledge',[owner,'lamp-review',review.digest],false);
fs.writeFileSync('public/deployment.json',JSON.stringify({...evidence,address:s.address,reviewId:'lamp-review'},null,2));console.log('COMPLETE',s.address);
