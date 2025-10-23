

Run();

static void Run()
{
    Combinator solution = new();

    Console.WriteLine("Input: n = 4, k = 2");
    var result1 = solution.Combine(4, 2);
    Console.WriteLine($"Output: {FormatResult(result1)}");

}

static string FormatResult(IList<IList<int>> result)
{
    var combinations = new List<string>();
    foreach (var combo in result)
    {
        combinations.Add($"[{string.Join(",", combo)}]");
    }
    return $"[{string.Join(",", combinations)}]";
}


public class Combinator
{
    public IList<IList<int>> Combine(int n, int k)
    {
        IList<IList<int>> result = new List<IList<int>>();
        Backtrack(1, n, k, new List<int>(), result);
        return result;
    }

    private void Backtrack(int start, int n, int k, List<int> path, IList<IList<int>> result)
    {
        if (path.Count == k)
        {
            result.Add(new List<int>(path));
            return;
        }

        for (int i = start; i <= n; i++)
        {
            path.Add(i);
            Backtrack(i + 1, n, k, path, result);
            path.RemoveAt(path.Count - 1);
        }
    }
}

