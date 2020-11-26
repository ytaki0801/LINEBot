#
# JMC Lisp: defined in McCarthy's 1960 paper,
# with S-expression input/output and basic list processing
#


# basic list processing: cons, car, cdr, eq, atom

def cons(x, y): return (x, y)
def car(s): return s[0]
def cdr(s): return s[1]
def eq(s1, s2): return s1 == s2
def atom(s): return isinstance(s, str) or eq(s, None) or isinstance(s, bool)


# S-expression input: s_read

def s_lex(s):
    for p in "()'": s = s.replace(p, " " + p + " ")
    return s.split()

def s_syn(s):
    def quote(x):
        if len(s) != 0 and s[-1] == "'":
            del s[-1]
            return cons("quote", cons(x, None))
        else: return x
    t = s[-1]
    del s[-1]
    if t == ")":
        r = None
        while s[-1] != "(":
            if s[-1] == ".":
                del s[-1]
                r = cons(s_syn(s), car(r))
            else: r = cons(s_syn(s), r)
        del s[-1]
        return quote(r)
    else: return quote(t)

def s_read(s): return s_syn(s_lex(s))


# S-expression output: s_string

def s_strcons(s):
    sa_r = s_string(car(s))
    sd = cdr(s)
    if eq(sd, None):
        return sa_r
    elif atom(sd):
        return sa_r + " . " + sd
    else:
        return sa_r + " " + s_strcons(sd)

def s_string(s):
    if   eq(s, None):  return "()"
    elif eq(s, True):  return "t"
    elif eq(s, False): return "nil"
    elif atom(s):
        return s
    else:
        return "(" + s_strcons(s) + ")"


# JMC Lisp evaluator: s_eval

def caar(x): return car(car(x))
def cadr(x): return car(cdr(x))
def cadar(x): return car(cdr(car(x)))
def caddr(x): return car(cdr(cdr(x)))
def caddar(x): return car(cdr(cdr(car(x))))

def s_null(x): return eq(x, None)

def s_append(x, y):
    if s_null(x): return y
    else: return cons(car(x), s_append(cdr(x), y))

def s_list(x, y): return cons(x, cons(y, None))

def s_pair(x, y):
    if s_null(x) and s_null(y): return None
    elif (not atom(x)) and (not atom(y)):
        return cons(s_list(car(x), car(y)), s_pair(cdr(x), cdr(y)))

def s_assoc(x, y):
    if eq(caar(y), x): return cadar(y)
    else: return s_assoc(x, cdr(y))

def s_eval(e, a):
    if   eq(e, "t"):   return True
    elif eq(e, "nil"): return False
    elif atom(e): return s_assoc(e, a)
    elif atom(car(e)):
        if   eq(car(e), "quote"): return cadr(e)
        elif eq(car(e), "atom"):  return atom(s_eval(cadr(e), a))
        elif eq(car(e), "eq"):    return eq(  s_eval(cadr(e), a),
                                              s_eval(caddr(e), a))
        elif eq(car(e), "car"):   return car( s_eval(cadr(e), a))
        elif eq(car(e), "cdr"):   return cdr( s_eval(cadr(e), a))
        elif eq(car(e), "cons"):  return cons(s_eval(cadr(e), a),
                                              s_eval(caddr(e), a))
        elif eq(car(e), "cond"):  return evcon(cdr(e), a)
        else: return s_eval(cons(s_assoc(car(e), a), cdr(e)), a)
    elif eq(caar(e), "lambda"):
        return s_eval(caddar(e),
                      s_append(s_pair(cadar(e), evlis(cdr(e), a)), a))
    else: print("Error")

def evcon(c, a):
    if s_eval(caar(c), a): return s_eval(cadar(c), a)
    else: return evcon(cdr(c), a)

def evlis(m, a):
    if s_null(m): return None
    else: return cons(s_eval(car(m), a), evlis(cdr(m), a))


# REP (no Loop): s_rep
def s_rep(e): return s_string(s_eval(s_read(e), s_read("()")))

