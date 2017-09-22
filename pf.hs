import Data.List
import Data.Maybe
alpha = ['A'..'I'] ++ ['K'..'Z']

maybeFun :: (a -> a -> a) -> Maybe a -> a -> Maybe a
maybeFun _ Nothing _ = Nothing
maybeFun f x y = Just (fromJust x `f` y)

findPos :: Char -> [Char] -> Maybe Int
findPos char str = char `elemIndex` str

findCol :: Maybe Int -> Maybe Int
findCol x = maybeFun mod x 5 

findRow :: Maybe Int -> Maybe Int
findRow x = maybeFun div x 5



-- encode :: (Char, Char) -> [Char] -> (Char, Char)

