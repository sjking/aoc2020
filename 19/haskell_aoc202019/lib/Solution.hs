module Solution
  ( Trie(..)
  , buildTrie
  , parseInput
  , search
  )
  where

import Data.Map (Map)
import qualified Data.Map as M
import Text.Read (readMaybe)
import Data.Maybe (fromJust)

data Trie =
  Trie { terminal :: Bool
       , children :: Map Char Trie
       }
       deriving (Show, Eq)


type Rules = Map String [[String]]
type Message = String


empty :: Trie
empty = Trie False M.empty


buildTrie :: [String] -> Trie
buildTrie = foldr insert (Trie False M.empty)
  where
    insert :: String -> Trie -> Trie
    insert [] trie = trie {terminal=True}
    insert (c : cs) trie =
      let
        child = children trie
      in case M.lookup c child of
           Nothing    -> trie {children = M.insert c (insert cs empty) child}
           Just trie' -> trie {children = M.insert c (insert cs trie') child}


parseInput :: String -> (Rules, [Message])
parseInput = parseMessages [] . parseRules mempty . lines
  where
    addRule :: String -> (String, String, [String], [[String]]) -> Rules -> Rules
    addRule [] (n, curr, g, gs) rules = M.insert n (reverse $ (reverse (curr : g)) : gs) rules
    addRule (':' : rest) (_, curr, _, _) rules = addRule rest (curr, "", [], []) rules
    addRule (' ' : rest) (n, curr, g, gs) rules =
      if length curr == 0 then addRule rest (n, curr, g, gs) rules
                          else addRule rest (n, "", curr : g, gs) rules
    addRule ('"' : rest) memo rules = addRule rest memo rules
    addRule ('|' : rest) (n, _, g, gs) rules = addRule rest (n, "", [], (reverse g) : gs) rules
    addRule (c : rest) (n, curr, g, gs) rules = addRule rest (n, c : curr, g, gs) rules

    parseRules :: Rules -> [String] -> (Rules, [String])
    parseRules _ [] = undefined
    parseRules rules ("" : rest) = (rules, rest)
    parseRules rules (line : rest) = parseRules (addRule line ("", "", [], []) rules) rest

    parseMessages :: [Message] -> (Rules, [String]) -> (Rules, [Message])
    parseMessages messages (rules, []) = (rules, messages)
    parseMessages messages (rules, (m : ms)) = parseMessages (m : messages) (rules, ms)

search :: Rules -> Trie-> [Trie]
search rules trie =
  let
    tries = search' "0" rules [trie]
  in
    filter terminal tries

search' :: String -> Rules -> [Trie] -> [Trie]
search' c rules tries =
  case (readMaybe c :: Maybe Int) of
    Nothing ->
      let
        ch :: Char
        ch = head c
      in
        map fromJust . filter (not . null) . map (\t -> M.lookup ch (children t)) $ tries
    Just _ ->
      let
        groups :: [[String]]
        groups = fromJust $ M.lookup c rules

        traverseGroups :: [[String]] -> [[Trie]] -> [Trie]
        traverseGroups [] ts = concat . reverse $ ts
        traverseGroups (g : gs) ts = traverseGroups gs (traverseGroup g tries : ts)

        isWord :: Trie -> Bool
        isWord trie = terminal trie

        traverseGroup :: [String] -> [Trie] -> [Trie]
        traverseGroup [] ts = ts
        traverseGroup (c' : cs') ts =
          let
            children' = if length ts == 0 then []
                                          else search' c' rules ts
          in
            case cs' of
              [] -> children'
              _ -> traverseGroup cs' $ filter (not . isWord) children'
      in
        traverseGroups groups []

