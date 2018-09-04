(define (domain IPASS)

(:requirements :typing :equality)

;; TYPES

(:types
normal deficiency_course other_course - course
foundations_course systems_course applications_course - normal
specialization
concentration
professor
num
)

;; PREDICATES

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

;; ACTIONS / OPERATORS
{}

)
