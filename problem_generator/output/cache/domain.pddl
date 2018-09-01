(define (domain IPASS)

(:requirements :typing :equality)

(:types
normal deficiency other - course
foundations systems applications - normal
professor
num
)

(:predicates
(has_committee_chair ?p - professor) ; ?p is committee chair
(has_committee_chair_done) ; has picked committee chair
(has_committee ?p1 ?p2 ?p3 - professor) ; ?p1 ?p2 ?p3 are committee members
(has_committee_done) ; has picked all committee members
(requires ?c1 ?c2 - course) ; course ?c2 requires course ?c1
(has_taken ?c - course) ; taken course ?c
(completed_foundations) ; completed foundations requirement
(completed_systems) ; completed systems requirement
(completed_applications) ; completed applications requirement
(is_international) ; is an international student
(is_ra_ta) ; is an RA or TA
(defended) ; completed defense
(is_foundations ?p - professor) ; professor in foundations area
(is_systems ?p - professor) ; professor in systems area
(is_applications ?p - professor) ; professor in applications area
(specialized_in_big_data) ; optional specialization in big data
(specialized_in_cybersecurity) ; optional specialization in cybersecurity
(specialized_in_ai) ; optional specialization in ai
(courses_completed) ; 10 courses completed
(current_num ?n - num) ; objectified number line
(next_num ?n1 ?n2 - num) ; transitions between consecutive numbers
(sem_quota ?n - num) ; counter for courses within a semester
(completed_deficiencies) ; completed all deficiency courses
(selected ?p - professor) ; selected professor for committee
(has_committee_member2 ?p - professor) ; selected first committee member
(has_committee_member3 ?p - professor) ; selected second committee member
(ready_to_complete_semester)
)

; taking a nomral course increments global course counter + semester course counter
; requires you to have completed all deficiencies 
; cannot do more than four in a semester and cannot repeat same course twice

(:action take_normal_course
:parameters (?c - normal ?n1 ?n2 - num ?s1 ?s2 - num)
:precondition (and
(not (has_taken ?c))
(next_num ?n1 ?n2)
(current_num ?n1)
(sem_quota ?s1)
(next_num ?s1 ?s2)
(not (sem_quota four))
(completed_deficiencies)
)
:effect (and
(has_taken ?c)
(current_num ?n2)
(not (current_num ?n1))
(sem_quota ?s2)
(not (sem_quota ?s1))
)
)

; taking a deficiency course increments ONLY semester course counter

(:action take_deficiency_course
:parameters (?c - deficiency ?n1 ?n2 - num ?s1 ?s2 - num)
:precondition (and
(not (has_taken ?c))
(sem_quota ?s1)
(next_num ?s1 ?s2)
(not (sem_quota four))
)
:effect (and
(has_taken ?c)
(sem_quota ?s2)
(not (sem_quota ?s1))
)
)

; completion of all deficiencies are needed before other courses

(:action complete_deficiency
:parameters ()
:precondition (and
(has_taken CSE340)
(has_taken CSE360)
(has_taken CSE310)
(has_taken CSE230)
(has_taken CSE330)
(has_taken CSE355)
)
:effect (and
(completed_deficiencies)
)
)

; First Thesis course only possible after selection of chair
; other properties same as normal courses

(:action take_CSE599a
:parameters (?n1 ?n2 - num ?s1 ?s2 - num)
:precondition (and
(not (has_taken CSE599a))
(next_num ?n1 ?n2)
(current_num ?n1)
(sem_quota ?s1)
(next_num ?s1 ?s2)
(not (sem_quota four))
(has_committee_chair_done)
(completed_deficiencies)
)
:effect (and
(has_taken CSE599a)
(current_num ?n2)
(not (current_num ?n1))
(sem_quota ?s2)
(not (sem_quota ?s1))
)
)

; Second Thesis course only possible at the end
; other properties same as normal courses

(:action take_CSE599b
:parameters (?n1 ?n2 - num ?s1 ?s2 - num)
:precondition (and
(not (has_taken CSE599b))
(next_num ?n1 ?n2)
(current_num ?n1)
(sem_quota ?s1)
(next_num ?s1 ?s2)
(not (sem_quota four))
(has_committee_done)
(current_num nine)
(completed_deficiencies)
)
:effect (and
(has_taken CSE599b)
(current_num ?n2)
(not (current_num ?n1))
(sem_quota ?s2)
(not (sem_quota ?s1))
)
)

; complete semester with one course
; resets semester course count to zero
; cannot do if international or RA/TA

(:action complete_sem_1
:parameters ()
:precondition (and
(sem_quota one)
(not (is_international))
(not (is_ra_ta))
)
:effect (and
(ready_to_complete_semester)
(not (sem_quota one))
)
)

; complete semester with two courses
; resets semester course count to zero
; cannot do if international or RA/TA

(:action complete_sem_2
:parameters ()
:precondition (and
(sem_quota two)
(not (is_international))
(not (is_ra_ta))
)
:effect (and
(ready_to_complete_semester)
(not (sem_quota two))
)
)

; complete semester with three courses
; resets semester course count to zero

(:action complete_sem_3
:parameters ()
:precondition (and
(sem_quota three)
)
:effect (and
(ready_to_complete_semester)
(not (sem_quota three))
)
)

; complete semester with four courses
; can only do if RA/TA

(:action complete_sem_4
:parameters ()
:precondition (and
(sem_quota four)
(is_ra_ta)
)
:effect (and
(ready_to_complete_semester)
(not (sem_quota four))
)
)

; complete semester on the interface

(:action complete_semester
:parameters ()
:precondition (and
(ready_to_complete_semester)
)
:effect (and
(not (ready_to_complete_semester))
(sem_quota one)
)
)

; complete one course from foundations

(:action complete_foundations
:parameters (?f - foundations)
:precondition (and
(has_taken ?f)
)
:effect (and
(completed_foundations)
)
)

; complete one course from systems

(:action complete_systems
:parameters (?s - systems)
:precondition (and
(has_taken ?s)
)
:effect (and
(completed_systems)
)
)

; complete one course from applications

(:action complete_applications
:parameters (?a - applications)
:precondition (and
(has_taken ?a)
)
:effect (and
(completed_applications)
)
)

; select committee chair

(:action select_committee_chair
:parameters (?p - professor)
:precondition (and
(not (has_committee_chair_done))
(not (selected ?p))
)
:effect (and
(selected ?p)
(has_committee_chair ?p)
(has_committee_chair_done)
)
)

; select second committee member

(:action select_committee_member_2
:parameters (?p - professor)
:precondition (and
(not (selected ?p))
(not (has_committee_member2 ?p))
)
:effect (and
(selected ?p)
(has_committee_member2 ?p)
)
)

; select third committee member

(:action select_committee_member_3
:parameters (?p - professor)
:precondition (and
(not (selected ?p))
(not (has_committee_member3 ?p))
)
:effect (and
(selected ?p)
(has_committee_member3 ?p)
)
)

; finalize committee

(:action select_committee
:parameters (?p1 ?p2 ?p3 - professor)
:precondition (and
(not (has_committee_done))
(has_committee_chair ?p1)
(has_committee_member2 ?p2)
(has_committee_member3 ?p3)
)
:effect (and
(has_committee ?p1 ?p2 ?p3)
(has_committee_done)
)
)

; select specialization in big data
; must have chair in the same area

(:action specialize_big_data
:parameters (?p - professor)
:precondition (and
(has_committee_chair ?p)
(is_applications ?p)
(has_taken CSE510)
(has_taken CSE512)
(has_taken CSE572)
)
:effect (and
(specialized_in_big_data)
)
)

; select specialization in cybersecurity
; must have chair in the same area

(:action specialize_cybersecurity
:parameters (?p - professor)
:precondition (and
(has_committee_chair ?p)
(is_systems ?p)
(has_taken CSE543)
(has_taken CSE545)
(has_taken CSE548)
)
:effect (and
(specialized_in_cybersecurity)
)
)

; select specialization in AI
; must have chair in the same area

(:action specialize_ai
:parameters (?p - professor)
:precondition (and
(has_committee_chair ?p)
(is_applications ?p)
(has_taken CSE575)
(has_taken CSE574)
(has_taken CSE571)
)
:effect (and
(specialized_in_ai)
)
)

; defend!
; must have completed 8 normal courses + 599a/b
; must have finaled committee
; must have one course each from foundations systems and applications

(:action defend
:parameters ()
:precondition (and
(has_committee_done)
(completed_foundations)
(completed_systems)
(completed_applications)
(has_taken CSE599a)
(has_taken CSE599b)
(current_num ten)
(not (sem_quota four))
)
:effect (and
(defended)
)
)

)

