(define (problem masterplan) (:domain IPASS)

(:objects
Liu Candan Sarwat Zhang Doupe Colbourn Xue Richa Huang Rao Sen Amor - professor
zero one two three four five six seven eight nine ten - num
CSE340 CSE360 CSE310 CSE230 CSE330 CSE355 - deficiency
CSE569 CSE579 CSE556 CSE555 CSE551 CSE550 CSE552 - foundations
CSE543 CSE545 CSE548 CSE563 CSE565 CSE520 CSE522 CSE546 CSE561 CSE564 CSE566 CSE539 CSE531 CSE530 CSE536 CSE535 CSE534 - systems
CSE572 CSE571 CSE574 CSE509 CSE578 CSE511 CSE510 CSE512 CSE515 CSE570 CSE577 CSE573 CSE576 CSE575 - applications
CSE599a CSE599b - other
)

(:init
(current_sem zero)
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
(has_taken CSE340)
(has_taken CSE360)
(has_taken CSE310)
(has_taken CSE230)
(is_ra_ta)
;(is_international)
)

(:goal (and
(defended)
(specialized_in_cybersecurity)
(completed_deficiencies)
)
)

)
