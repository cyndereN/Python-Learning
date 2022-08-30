> (define s (cons 1 (cons 2 nil)))

> s
(1 2)

>(draw s)

> (cons 3 s)
(3 1 2)

> (cons (cons 4 (cons 3 nil)) s)
((4 3) 1 2)

> (car (cons (cons 4 (cons 3 nil)) s))
(4 3)

> (car (car (cons (cons 4 (cons 3 nil)) s)))
4

> (cons s (cons s nil))
((1 2) (1 2))

> (list? s)
#t

> (list 1 2 3 4)
(1 2 3 4)

> (cdr (list 1 2 3))
(2 3 4)

> (define b 2)

> '(a b c)
(a b c)

> (list 'a 'b 'c)
(a b c)

> `(a b c)
(a b c)

> `(a ,b c)
(a 2 c)


