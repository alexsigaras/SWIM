
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\xcb\xeb\xd2#\xce\x1e\x9fY%\x02P\xa6(3)\x17'
    
_lr_action_items = {'RPAREN':([3,9,10,11,20,21,22,23,24,25,26,28,29,],[-15,-16,-13,20,-14,-10,-11,-9,-7,-8,-12,30,31,]),'DIVIDE':([3,7,8,9,10,11,20,21,22,23,24,25,26,27,29,],[-15,12,-16,-16,-13,12,-14,-10,-11,-9,12,12,-12,12,12,]),'POW':([3,7,8,9,10,11,20,21,22,23,24,25,26,27,29,],[-15,13,-16,-16,13,13,-14,13,13,13,13,13,13,13,13,]),'NUMBER':([0,4,6,12,13,14,15,16,17,18,19,],[3,3,3,3,3,3,3,3,3,3,3,]),'ID':([0,4,6,12,13,14,15,16,17,18,19,],[8,9,9,9,9,9,9,9,9,9,9,]),'EQUALS':([8,],[18,]),'PLUS':([3,7,8,9,10,11,20,21,22,23,24,25,26,27,29,],[-15,15,-16,-16,-13,15,-14,-10,-11,-9,-7,-8,-12,15,15,]),'MOD':([3,7,8,9,10,11,20,21,22,23,24,25,26,27,29,],[-15,17,-16,-16,-13,17,-14,-10,-11,-9,17,17,-12,17,17,]),'LPAREN':([0,4,6,8,12,13,14,15,16,17,18,19,],[6,6,6,19,6,6,6,6,6,6,6,6,]),'STRING':([19,],[28,]),'TIMES':([3,7,8,9,10,11,20,21,22,23,24,25,26,27,29,],[-15,14,-16,-16,-13,14,-14,-10,-11,-9,14,14,-12,14,14,]),'MINUS':([0,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,29,],[4,-15,4,4,16,-16,-16,-13,16,4,4,4,4,4,4,4,4,-14,-10,-11,-9,-7,-8,-12,16,16,]),'$end':([1,2,3,5,7,8,9,10,20,21,22,23,24,25,26,27,30,31,],[-1,-2,-15,0,-6,-16,-16,-13,-14,-10,-11,-9,-7,-8,-12,-5,-3,-4,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'function':([0,],[1,]),'start':([0,],[5,]),'expression':([0,4,6,12,13,14,15,16,17,18,19,],[7,10,11,21,22,23,24,25,26,27,29,]),'statement':([0,],[2,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> function','start',1,'p_start','swim.py',85),
  ('start -> statement','start',1,'p_start','swim.py',86),
  ('function -> ID LPAREN STRING RPAREN','function',4,'p_function','swim.py',89),
  ('function -> ID LPAREN expression RPAREN','function',4,'p_function','swim.py',90),
  ('statement -> ID EQUALS expression','statement',3,'p_statement_assign','swim.py',96),
  ('statement -> expression','statement',1,'p_statement_expr','swim.py',100),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','swim.py',104),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','swim.py',105),
  ('expression -> expression TIMES expression','expression',3,'p_expression_binop','swim.py',106),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','swim.py',107),
  ('expression -> expression POW expression','expression',3,'p_expression_binop','swim.py',108),
  ('expression -> expression MOD expression','expression',3,'p_expression_binop','swim.py',109),
  ('expression -> MINUS expression','expression',2,'p_expression_uminus','swim.py',131),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','swim.py',135),
  ('expression -> NUMBER','expression',1,'p_expression_number','swim.py',139),
  ('expression -> ID','expression',1,'p_expression_name','swim.py',144),
]
