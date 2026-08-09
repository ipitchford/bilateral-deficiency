import Std.Tactic.BVDecide

/-!
Parser-independent finite verification of the terminal signature of the
SAT 2024 E_(3,2,2) enforcer.  Variables are numbered 0,...,7 here, so the
distinguished terminal x_1 is variable 0.
-/

inductive TriState where
  | unassigned
  | false
  | true
  deriving BEq, DecidableEq, Repr

inductive TerminalMask where
  | none
  | positive
  | negative
  | both
  deriving BEq, DecidableEq, Repr

structure Literal where
  varId : Nat
  positive : Bool
  deriving BEq, DecidableEq, Repr

abbrev Clause := List Literal
abbrev Assignment := List TriState

structure SignatureRow where
  state : TriState
  mask : TerminalMask
  value : Int
  deriving BEq, DecidableEq, Repr

def neg (varId : Nat) : Literal := { varId, positive := false }
def pos (varId : Nat) : Literal := { varId, positive := true }

def enforcer : List Clause :=
  [ [neg 0, neg 3, neg 7]
  , [neg 1, neg 5, neg 7]
  , [neg 0, neg 5, pos 7]
  , [neg 3, neg 6, pos 7]
  , [neg 2, neg 4, pos 6]
  , [neg 1, pos 4, pos 5]
  , [neg 2, pos 3, neg 6]
  , [pos 2, neg 4, pos 5]
  , [pos 1, pos 4, pos 6]
  , [pos 1, pos 2, pos 3]
  ]

def states : List TriState :=
  [.false, .true, .unassigned]

def masks : List TerminalMask :=
  [.none, .positive, .negative, .both]

def assignments : Nat → List Assignment
  | 0 => [[]]
  | n + 1 =>
      states.flatMap fun state =>
        (assignments n).map fun tail => state :: tail

def stateAt (assignment : Assignment) (varId : Nat) : TriState :=
  (assignment[varId]?).getD .unassigned

def literalSatisfied (assignment : Assignment) (literal : Literal) : Bool :=
  match stateAt assignment literal.varId with
  | .unassigned => false
  | .false => !literal.positive
  | .true => literal.positive

def clauseSurvives (assignment : Assignment) (clause : Clause) : Bool :=
  !(clause.any (literalSatisfied assignment))

def residualOccurrence
    (assignment : Assignment) (varId : Nat) (positive : Bool) : Bool :=
  enforcer.any fun clause =>
    clauseSurvives assignment clause &&
      clause.any fun literal =>
        literal.varId == varId &&
          literal.positive == positive &&
          stateAt assignment varId == .unassigned

def internallyBilateral (assignment : Assignment) : Bool :=
  (List.range 7).all fun offset =>
    let varId := offset + 1
    stateAt assignment varId != .unassigned ||
      (residualOccurrence assignment varId true &&
       residualOccurrence assignment varId false)

def terminalMask (assignment : Assignment) : TerminalMask :=
  if stateAt assignment 0 != .unassigned then
    .none
  else
    match residualOccurrence assignment 0 true,
          residualOccurrence assignment 0 false with
    | false, false => .none
    | true, false => .positive
    | false, true => .negative
    | true, true => .both

def localCost (assignment : Assignment) : Int :=
  let surviving := (enforcer.filter (clauseSurvives assignment)).length
  let unassignedInternal :=
    ((List.range 7).filter fun offset =>
      stateAt assignment (offset + 1) == .unassigned).length
  Int.ofNat surviving - Int.ofNat unassignedInternal

def minimum? : List Int → Option Int
  | [] => none
  | value :: values => some (values.foldl min value)

def signatureRow? (state : TriState) (mask : TerminalMask) : Option SignatureRow :=
  let costs :=
    (assignments 8).filterMap fun assignment =>
      if internallyBilateral assignment &&
          stateAt assignment 0 == state &&
          terminalMask assignment == mask then
        some (localCost assignment)
      else
        none
  (minimum? costs).map fun value => { state, mask, value }

def computedSignature : List SignatureRow :=
  states.flatMap fun state =>
    masks.filterMap fun mask => signatureRow? state mask

def expectedSignature : List SignatureRow :=
  [ { state := .false, mask := .none, value := 0 }
  , { state := .true, mask := .none, value := 1 }
  , { state := .unassigned, mask := .none, value := 1 }
  , { state := .unassigned, mask := .negative, value := 1 }
  ]

theorem enforcer_terminal_signature_exact :
    computedSignature = expectedSignature := by
  native_decide

def main : IO Unit := do
  IO.println s!"checked assignments: {(assignments 8).length}"
  IO.println s!"computed signature: {repr computedSignature}"
  if computedSignature == expectedSignature then
    IO.println "s LEAN_TERMINAL_SIGNATURE_VERIFIED"
  else
    throw <| IO.userError "terminal signature mismatch"
