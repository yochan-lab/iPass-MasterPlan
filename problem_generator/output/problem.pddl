(define (problem masterplan) (:domain IPASS)

(:objects
zero one two three four five six seven eight nine ten - num
foundations systems applications - concentration
big_data ai cybersecurity - specialization
Liu Candan Sarwat Zhang Doupe Colbourn Xue Richa Huang Rao Sen Amor - professor
CSE340 CSE360 CSE310 CSE230 CSE330 CSE355 - deficiency_course
CSE509 CSE578 CSE511 CSE510 CSE512 CSE515 CSE572 CSE571 CSE570 CSE577 CSE573 CSE576 CSE575 CSE574 - applications_course
CSE599a CSE599b CSE592 - other_course
CSE563 CSE565 CSE520 CSE522 CSE548 CSE546 CSE561 CSE545 CSE564 CSE543 CSE566 CSE539 CSE531 CSE530 CSE536 CSE535 CSE534 - systems_course
CSE569 CSE579 CSE556 CSE551 CSE550 CSE552 CSE555 - foundations_course

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
(next_num ten ten)
(is_concentration CSE563 systems)
(is_concentration CSE565 systems)
(is_concentration CSE509 applications)
(is_concentration CSE520 systems)
(is_concentration CSE522 systems)
(is_concentration CSE569 foundations)
(is_concentration CSE548 systems)
(is_concentration CSE546 systems)
(is_concentration CSE561 systems)
(is_concentration CSE545 systems)
(is_concentration CSE564 systems)
(is_concentration CSE543 systems)
(is_concentration CSE566 systems)
(is_concentration CSE579 foundations)
(is_concentration CSE578 applications)
(is_concentration CSE511 applications)
(is_concentration CSE510 applications)
(is_concentration CSE539 systems)
(is_concentration CSE512 applications)
(is_concentration CSE515 applications)
(is_concentration CSE572 applications)
(is_concentration CSE571 applications)
(is_concentration CSE570 applications)
(is_concentration CSE531 systems)
(is_concentration CSE530 systems)
(is_concentration CSE536 systems)
(is_concentration CSE535 systems)
(is_concentration CSE534 systems)
(is_concentration CSE577 applications)
(is_concentration CSE573 applications)
(is_concentration CSE576 applications)
(is_concentration CSE575 applications)
(is_concentration CSE556 foundations)
(is_concentration CSE551 foundations)
(is_concentration CSE550 foundations)
(is_concentration CSE552 foundations)
(is_concentration CSE555 foundations)
(is_concentration CSE574 applications)

(is_expert Liu big_data)
(is_expert Candan cybersecurity)
(is_expert Sarwat big_data)
(is_expert Zhang ai)
(is_expert Doupe cybersecurity)
(is_expert Xue big_data)
(is_expert Huang cybersecurity)
(is_expert Rao ai)
(is_expert Amor ai)

(has_taken CSE310)
(has_taken CSE230)


(has_taken CSE330)
(has_taken CSE355)

(is_international)
)

(:goal (and
(defended)
)
)

)