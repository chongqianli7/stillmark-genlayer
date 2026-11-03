import sys,types,unittest,importlib.util,json
from pathlib import Path
class Return:
 def __init__(self,v):self.calldata=v
class Error(Exception):pass
sender=types.SimpleNamespace(sender_address='0x'+'1'*40)
answers=[]
last_validator=None
def nondet(leader,validator):
 global last_validator
 last_validator=validator
 result=leader()
 if not validator(Return(result)):raise Error('DISAGREEMENT')
 return result
host=types.SimpleNamespace(Contract=object,public=types.SimpleNamespace(write=lambda f:f,view=lambda f:f),vm=types.SimpleNamespace(UserError=Error,Return=Return,run_nondet_unsafe=nondet),message=sender,nondet=types.SimpleNamespace(exec_prompt=lambda *a,**k:answers.pop(0)))
sys.modules['genlayer']=types.SimpleNamespace(gl=host,TreeMap=dict)
spec=importlib.util.spec_from_file_location('contract',Path(__file__).parents[1]/'contracts/stillmark.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
A,B,C=['0x'+s*40 for s in '123']
BEFORE='Lamp tag CL-204. Shade intact. Stem straight. Base scratched.'
AFTER='Lamp tag CL-204. Shade intact. Stem dented. Base scratched.'
PARTS=['Shade','Stem','Base']
def matrix(labels=('UNCHANGED','NEW_DAMAGE','UNCHANGED'),identity='SAME'):
 return dict(identity=identity,findings=[dict(part=p,label=l,before_quote=b,after_quote=a) for p,l,b,a in zip(PARTS,labels,['Shade intact','Stem straight','Base scratched'],['Shade intact','Stem dented','Base scratched'])])
class Tests(unittest.TestCase):
 def setUp(self):
  answers.clear();sender.sender_address=A;self.r=c.Stillmark();self.r.dispatch('lamp',B,'Lamp tag CL-204',json.dumps(PARTS),BEFORE)
 def get(self):return json.loads(self.r.get_record(A,'lamp'))
 def received(self):sender.sender_address=B;self.r.receive(A,'lamp',AFTER)
 def compared(self,labels=('UNCHANGED','NEW_DAMAGE','UNCHANGED'),identity='SAME'):
  self.received();answers.extend([matrix(labels,identity),matrix(labels,identity)]);self.r.compare(A,'lamp')
 def test_dispatch_immutable_and_namespaced(self):
  with self.assertRaisesRegex(Error,'ID_USED'):self.r.dispatch('lamp',B,'Lamp tag CL-204',json.dumps(PARTS),BEFORE)
  sender.sender_address=B;self.r.dispatch('lamp',A,'Lamp tag CL-204',json.dumps(PARTS),BEFORE)
  self.assertEqual(json.loads(self.r.get_record(B,'lamp'))['owner'],B)
 def test_receiver_only_and_once(self):
  with self.assertRaisesRegex(Error,'ONLY_RECEIVER'):self.r.receive(A,'lamp',AFTER)
  self.received()
  with self.assertRaisesRegex(Error,'LOCKED'):self.r.receive(A,'lamp',AFTER)
 def test_no_comparison_before_receipt(self):
  with self.assertRaisesRegex(Error,'NOT_RECEIVED'):self.r.compare(A,'lamp')
 def test_full_bilateral_acknowledgement(self):
  self.compared();r=self.get();self.assertEqual(r['status'],'EXCEPTIONS');self.r.acknowledge(A,'lamp',r['digest']);self.assertEqual(self.get()['status'],'EXCEPTIONS')
  sender.sender_address=A;self.r.acknowledge(A,'lamp',r['digest']);self.assertEqual(self.get()['status'],'ACKNOWLEDGED')
  with self.assertRaisesRegex(Error,'TERMINAL'):self.r.decline(A,'lamp')
 def test_stale_digest_and_duplicate_signature(self):
  self.compared()
  with self.assertRaisesRegex(Error,'STALE'):self.r.acknowledge(A,'lamp','bad')
  self.r.acknowledge(A,'lamp',self.get()['digest'])
  with self.assertRaisesRegex(Error,'ALREADY'):self.r.acknowledge(A,'lamp',self.get()['digest'])
 def test_uncertain_part_and_identity_each_block(self):
  for result in [matrix(('UNCHANGED','UNCLEAR','UNCHANGED')),matrix(identity='UNCLEAR')]:
   self.assertEqual(c.decision(result),'REVIEW')
  self.compared(('UNCHANGED','UNCLEAR','UNCHANGED'))
  with self.assertRaisesRegex(Error,'NOT_ACKNOWLEDGEABLE'):self.r.acknowledge(A,'lamp',self.get()['digest'])
 def test_agreement_on_aggregate_is_not_enough(self):
  self.received();answers.extend([matrix(),matrix(('NEW_DAMAGE','UNCHANGED','UNCHANGED'))])
  with self.assertRaisesRegex(Error,'DISAGREEMENT'):self.r.compare(A,'lamp')
  self.assertEqual(self.get()['status'],'RECEIVED')
 def test_identity_disagreement_blocks(self):
  self.received();answers.extend([matrix(),matrix(identity='UNCLEAR')])
  with self.assertRaisesRegex(Error,'DISAGREEMENT'):self.r.compare(A,'lamp')
 def test_quotes_and_part_order_are_enforced(self):
  for mutate in [lambda r:r['findings'][0].update(before_quote='fabricated evidence'),lambda r:r['findings'].reverse(),lambda r:r['findings'][0].update(label='SAFE')]:
   r=matrix();mutate(r)
   with self.assertRaises(Error):c.parse_findings(r,PARTS,BEFORE,AFTER)
 def test_nonparty_cannot_compare_ack_or_decline(self):
  self.compared();sender.sender_address=C
  for fn,args in [(self.r.compare,(A,'lamp')),(self.r.acknowledge,(A,'lamp',self.get()['digest'])),(self.r.decline,(A,'lamp'))]:
   with self.assertRaisesRegex(Error,'ONLY_PARTIES'):fn(*args)
 def test_decline_locks_history(self):
  self.r.decline(A,'lamp');self.assertEqual(self.get()['declined_by'],A);sender.sender_address=B
  with self.assertRaisesRegex(Error,'LOCKED'):self.r.receive(A,'lamp',AFTER)
 def test_validator_nonreturn_or_malformed_never_accepts(self):
  self.compared();self.assertFalse(last_validator(None));self.assertFalse(last_validator(Return('{}')))
 def test_unchanged_and_improved_are_distinct(self):
  self.assertEqual(c.decision(matrix(('UNCHANGED',)*3)),'CONSISTENT');self.assertEqual(c.decision(matrix(('IMPROVED',)*3)),'EXCEPTIONS')
 def test_sender_and_bounds(self):
  for receiver,parts in [(A,PARTS),(B,[]),(B,['Stem','stem'])]:
   with self.assertRaises(Error):self.r.dispatch('invalid',receiver,'Lamp tag CL-204',json.dumps(parts),BEFORE)
if __name__=='__main__':unittest.main()
