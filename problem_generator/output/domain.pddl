(define (domain IPASS)

(:requirements :typing :equality)

(:types
normal deficiency_course other_course - course
foundations_course systems_course applications_course - normal
specialization
concentration
professor
num
)

(:predicates

(selected ?p - professor)                              ; selected professor for committee
(has_committee_chair ?p - professor)                   ; ?p is committee chair
(has_committee_chair_done)                             ; has committee chair
(has_committee_member2)                                ; selected first committee member
(has_committee_member3)                                ; selected second committee member
(has_committee_done)                                   ; has committee

(is_concentration ?c - normal ?x - concentration)      ; normal course ?c has concentration ?x
(has_taken ?c - course)                                ; taken course ?c

(is_international)                                     ; is an international student
(is_ra_ta)                                             ; is an RA or TA

(is_expert ?p - professor ?x - specialization)         ; professor ?p in ?x area
(chair_expertise ?x - specialization)                  ; expertise ?x of chair established

(courses_completed)                                    ; 10 courses completed
(current_num ?n - num)                                 ; objectified number line
(next_num ?n1 ?n2 - num)                               ; transitions between consecutive numbers
(sem_quota ?n - num)                                   ; counter for courses within a semester

(ready_to_complete_semester)                           ; for super completer of semesters
(completed_concentration ?x - concentration)           ; completed each concentration of foundation system and application
(completed_specialization)                             ; completed specialization in any one of ai, big data or cybersecurity
(defended)                                             ; completed defense

)

; taking a nomral course increments global course counter + semester course counter
; requires you to have completed all deficiencies 
; cannot do more than four in a semester and cannot repeat same course twice

(:action take_normal_course
:parameters (?c - normal ?x - concentration ?n1 ?n2 - num ?s1 ?s2 - num)
:precondition (and
(not (has_taken ?c))
(next_num ?n1 ?n2)
(current_num ?n1)
(sem_quota ?s1)
(next_num ?s1 ?s2)
(not (sem_quota four))
(is_concentration ?c ?x)
(has_taken CSE340)
(has_taken CSE360)
(has_taken CSE310)
(has_taken CSE230)
(has_taken CSE330)
(has_taken CSE355)
(not (sem_quota four))
(not (current_num ten))
)
:effect (and
(has_taken ?c)
(current_num ?n2)
(not (current_num ?n1))
(sem_quota ?s2)
(not (sem_quota ?s1))
(completed_concentration ?x)
)
)

; taking a deficiency course increments ONLY semester course counter

(:action take_deficiency_course
:parameters (?c - deficiency_course ?n1 ?n2 - num ?s1 ?s2 - num)
:precondition (and
(not (has_taken ?c))
(next_num ?n1 ?n2)
(current_num ?n1)
(sem_quota ?s1)
(next_num ?s1 ?s2)
(not (sem_quota four))
(not (current_num ten))
)
:effect (and
(has_taken ?c)
(sem_quota ?s2)
(not (sem_quota ?s1))
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
(has_taken CSE340)
(has_taken CSE360)
(has_taken CSE310)
(has_taken CSE230)
(has_taken CSE330)
(has_taken CSE355)
(not (sem_quota four))
(not (current_num ten))
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
(has_taken CSE340)
(has_taken CSE360)
(has_taken CSE310)
(has_taken CSE230)
(has_taken CSE330)
(has_taken CSE355)
(not (sem_quota four))
(not (current_num ten))
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

(:action complete_semester_1
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

(:action complete_semester_2
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

(:action complete_semester_3
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

(:action complete_semester_4
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
(not (sem_quota zero))
(not (sem_quota five))
(not (sem_quota six))
(not (sem_quota seven))
(not (sem_quota eight))
(not (sem_quota nine))
(not (sem_quota ten))
)
:effect (and
(not (ready_to_complete_semester))
(sem_quota zero)
)
)

; select committee chair

(:action select_committee_chair
:parameters (?p - professor ?x - specialization)
:precondition (and
(not (has_committee_chair_done))
(not (selected ?p))
(is_expert ?p ?x)
)
:effect (and
(selected ?p)
(has_committee_chair ?p)
(has_committee_chair_done)
(chair_expertise ?x)
)
)

; select second committee member

(:action select_committee_member_2
:parameters (?p - professor)
:precondition (and
(not (selected ?p))
(not (has_committee_member2))
)
:effect (and
(selected ?p)
(has_committee_member2)
)
)

; select third committee member

(:action select_committee_member_3
:parameters (?p - professor)
:precondition (and
(not (selected ?p))
(has_committee_member2)
(not (has_committee_member3))
)
:effect (and
(selected ?p)
(has_committee_member3)
(has_committee_done)
)
)

; select specialization in big data
; must have chair in the same area

(:action specialize_big_data
:parameters ()
:precondition (and
(has_committee_chair_done)
(chair_expertise big_data)
(has_taken CSE510)
(has_taken CSE512)
(has_taken CSE572)
(not (completed_specialization))
)
:effect (and
(completed_specialization)
)
)

; select specialization in cybersecurity
; must have chair in the same area

(:action specialize_cybersecurity
:parameters ()
:precondition (and
(has_committee_chair_done)
(chair_expertise cybersecurity)
(has_taken CSE543)
(has_taken CSE545)
(has_taken CSE548)
(not (completed_specialization))
)
:effect (and
(completed_specialization)
)
)

; select specialization in AI
; must have chair in the same area

(:action specialize_ai
:parameters ()
:precondition (and
(has_committee_chair_done)
(chair_expertise ai)
(has_taken CSE575)
(has_taken CSE574)
(has_taken CSE571)
(not (completed_specialization))
)
:effect (and
(completed_specialization)
)
)

; defend!
; must have completed 8 normal courses + 599a/b
; must have finaled committee
; must have one course each from foundations systems and applications

(:action defend
:parameters ()
:precondition (and
(has_committee_chair_done)
(has_committee_done)
(has_committee_member2)
(has_committee_member3)
(completed_specialization)
(completed_concentration foundations)
(completed_concentration systems)
(completed_concentration applications)
(has_taken CSE599a)
(has_taken CSE599b)
(current_num ten)
(not (sem_quota four))
)
:effect (and
(defended)
)
)

; dummy action make sure the domain generates
; complete semester 1 and 2 for non-international students 
(:action enable_all_complete_sem
:parameters ()
:precondition (and
(sem_quota ten)
)
:effect (and
(not (is_international))
(not (is_ra_ta))
)
)

; dummy action make sure the domain generates
; complete semester 4 for non ra students as well
; although it can not be done but this ensures we dont need
; to explicitly remove the action of four courses which
; are allowed.
(:action enable_all_complete_sem_2
:parameters ()
:precondition (and
(sem_quota ten)
)
:effect (and
(is_international)
(is_ra_ta)
)
)
)
