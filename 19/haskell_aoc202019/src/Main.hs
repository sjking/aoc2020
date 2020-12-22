import Solution (Trie(..), parseInput, buildTrie, search)
import Data.Map (Map)
import qualified Data.Map as M
import System.IO (openFile, IOMode(ReadMode), hGetContents)

main :: IO ()
main = do
  handle <- openFile "resources/input2" ReadMode
  contents <- hGetContents handle
  --putStrLn $ show $ lines contents
  let (rules, messages) = parseInput contents
  --putStrLn $ "Rules: " ++ (show rules)
  --putStrLn $ "Messages: " ++ (show messages)
  let trie = buildTrie messages
  --putStrLn $ show trie
  let result = search rules trie
  --putStrLn $ show result
  putStrLn $ "Part 1"
  putStrLn $ "Number of valid messages: " ++ (show . length $ result)
