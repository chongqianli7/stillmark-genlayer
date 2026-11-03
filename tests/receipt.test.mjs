import {test} from 'node:test';import assert from 'node:assert/strict';import {success,confirmedFailure,escapeHTML} from '../src/util.js';
const tx={status:'FINALIZED',result:'MAJORITY_AGREE',consensus_data:{leader_receipt:{mode:'leader',execution_result:'SUCCESS'}}};
test('finality alone never means successful execution',()=>{assert.equal(success(tx),true);assert.equal(success({...tx,status:'ACCEPTED'}),false);assert.equal(success({...tx,result:'MAJORITY_DISAGREE'}),false);assert.equal(success({...tx,consensus_data:{leader_receipt:{execution_result:'ERROR'}}}),false);});
test('failure requires terminal evidence',()=>{assert.equal(confirmedFailure({...tx,consensus_data:{leader_receipt:{execution_result:'ERROR'}}}),true);assert.equal(confirmedFailure({...tx,status:'PENDING',result:'NONE'}),false);});
test('public reports are escaped in HTML',()=>assert.equal(escapeHTML('<script>"&'), '&lt;script&gt;&quot;&amp;'));
