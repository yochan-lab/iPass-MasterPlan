(define (problem masterplan) (:domain IPASS)

(:objects
zero one two three four five six seven eight nine ten - num
Liu Candan Sarwat Zhang Doupe Colbourn Xue Richa Huang Rao Sen Amor - professor
CSE340 CSE360 CSE310 CSE230 CSE330 CSE355 - deficiency
CSE509 CSE578 CSE511 CSE510 CSE512 CSE515 CSE572 CSE571 CSE570 CSE577 CSE573 CSE576 CSE575 CSE574 - applications
CSE599a CSE599b CSE592 - other
CSE563 CSE565 CSE520 CSE522 CSE548 CSE546 CSE561 CSE545 CSE564 CSE543 CSE566 CSE539 CSE531 CSE530 CSE536 CSE535 CSE534 - systems
CSE569 CSE579 CSE556 CSE551 CSE550 CSE552 CSE555 - foundations

)

(:init
(sem_quota zero)
(current_num zero)
(next_num zero one)
(next_num one two)
(next_num two three)
(next_num three four)
(next_num four five)
(next_num five six)
(next_num six seven)
(next_num seven eight)
(next_num eight nine)
(next_num nine ten)
(is_applications Liu)
(is_systems Candan)
(is_systems Sarwat)
(is_applications Zhang)
(is_systems Doupe)
(is_foundations Colbourn)
(is_foundations Xue)
(is_foundations Richa)
(is_systems Huang)
(is_applications Rao)
(is_foundations Sen)
(is_applications Amor)
(has_taken CSE310)



(has_taken CSE330)
(has_taken CSE355)


)

(:goal (and
(specialized_in_cybersecurity)
(defended)
)
)

)
