grammar GlobalType;

spec        : globaltype EOF;

globaltype  : null_type | single_choice | PAROP choice_msg_exc PARCL | recursion | ref_rec_variable;

null_type   : ZERO;

choice_msg_exc : single_choice (CHOICE single_choice)*;
single_choice  : msg_exchange DOT globaltype;
msg_exchange : proc ARROW proc COLON msg;

recursion   : (RECURSION | MU) bind_rec_variable DOT globaltype;    // sanity check that globaltype is choice_msg_exc

bind_rec_variable : LOWCASESTART;
ref_rec_variable : LOWCASESTART;
proc        : UPPCASESTART;
msg         : LOWCASESTART;

RECURSION   : 'μ';
MU          : 'mu';
LOWCASESTART: [a-z] ([A-Za-z0-9])*;
UPPCASESTART: [A-Z] ([A-Za-z0-9])*;

ZERO        : '0';
ARROW       : '->';
PAROP       : '(';
PARCL       : ')';
COMMA       : ',';
DOT         : '.';
SEM         : ';';
COLON       : ':';
CHOICE      : '+';
WS          : [ \t\r\n]+ -> skip;
COMMENTS    : '//' ~('\r' | '\n')+ -> skip;
