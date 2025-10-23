
using NssfTechInterview.BusinessLogic;


BusinessLogic logic = new BusinessLogic();

var list = logic.GetCombinations(4, 2);

// Print the results
foreach (var combination in list)
{
    Console.Write("[" + string.Join(",", combination) + "]");
}
