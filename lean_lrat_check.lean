import Std.Sat.CNF
import Std.Tactic.BVDecide.LRAT

open Std Sat
open Std.Tactic.BVDecide

structure ParsedDimacs where
  cnf : CNF Nat
  declaredVariables : Nat
  declaredClauses : Nat

def nonemptyFields (line : String) : List String :=
  line.split Char.isWhitespace
    |>.filter (fun field => !field.isEmpty)
    |>.map (fun field => field.toString)
    |>.toList

def parseClauseLine (line : String) : Except String (CNF.Clause Nat) := do
  let fields := nonemptyFields line
  let literalFields ←
    match fields.reverse with
    | "0" :: reversed => pure reversed.reverse
    | _ => throw s!"clause line does not end in zero: {line}"
  let mut clause : CNF.Clause Nat := []
  for field in literalFields do
    let value ←
      match field.toInt? with
      | some value => pure value
      | none => throw s!"invalid DIMACS integer: {field}"
    if value == 0 then
      throw "zero appeared before the end of a clause"
    let identifier := value.natAbs
    if identifier == 0 then
      throw "DIMACS identifiers start at one"
    clause := (identifier - 1, value > 0) :: clause
  pure clause.reverse

def parseDimacs (text : String) : Except String ParsedDimacs := do
  let mut cnf : CNF Nat := .empty
  let mut declaredVariables := 0
  let mut declaredClauses := 0
  let mut foundHeader := false

  for rawLine in text.splitOn "\n" do
    let line := rawLine.trimAscii.toString
    if line.isEmpty || line.startsWith "c" then
      continue
    else if line.startsWith "p " then
      match nonemptyFields line with
      | ["p", "cnf", variableField, clauseField] =>
        let variableCount ←
          match variableField.toNat? with
          | some value => pure value
          | none => throw "invalid variable count in DIMACS header"
        let clauseCount ←
          match clauseField.toNat? with
          | some value => pure value
          | none => throw "invalid clause count in DIMACS header"
        declaredVariables := variableCount
        declaredClauses := clauseCount
        foundHeader := true
      | _ => throw s!"invalid DIMACS header: {line}"
    else
      cnf := cnf.add (← parseClauseLine line)

  if !foundHeader then
    throw "missing DIMACS header"
  if cnf.clauses.size != declaredClauses then
    throw s!"declared {declaredClauses} clauses but parsed {cnf.clauses.size}"
  for clause in cnf.clauses do
    for literal in clause do
      if literal.1 >= declaredVariables then
        throw s!"literal identifier {literal.1 + 1} exceeds the header"
  pure { cnf, declaredVariables, declaredClauses }

theorem lrat_success_implies_unsat
    (proof : Array LRAT.IntAction) (cnf : CNF Nat)
    (success : LRAT.check proof cnf) : cnf.Unsat :=
  LRAT.check_sound proof cnf success

def main (arguments : List String) : IO UInt32 := do
  match arguments with
  | [cnfPath, proofPath] =>
    let text ← IO.FS.readFile cnfPath
    let parsed ←
      match parseDimacs text with
      | .ok parsed => pure parsed
      | .error message =>
        IO.eprintln s!"c DIMACS parse failure: {message}"
        return 2
    let proof ← LRAT.loadLRATProof proofPath
    IO.println s!"c parsed {parsed.declaredVariables} variables and {parsed.declaredClauses} clauses"
    IO.println s!"c parsed {proof.size} LRAT actions"
    if success : LRAT.check proof parsed.cnf then
      let _unsat : parsed.cnf.Unsat :=
        LRAT.check_sound proof parsed.cnf success
      IO.println "s LEAN_LRAT_VERIFIED"
      return 0
    else
      IO.println "s LEAN_LRAT_NOT_VERIFIED"
      return 1
  | _ =>
    IO.eprintln "usage: lean --run lean_lrat_check.lean INPUT.cnf PROOF.lrat"
    return 2
