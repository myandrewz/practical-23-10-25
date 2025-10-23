

Run();

static void Run()
{
    Combinator solution = new();

    Console.WriteLine("Input: n = 4, k = 2");
    var result1 = solution.Combine(4, 2);
    Console.WriteLine($"Output: {FormatResult(result1)}");

}

static string FormatResult(List<List<int>> result)
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
    public List<List<int>> Combine(int n, int k)
    {
        List<List<int>> result = new List<List<int>>();
        Recurse(1, n, k, new List<int>(), result);
        return result;
    }

    private void Recurse(int start, int n, int k, List<int> path, List<List<int>> result)
    {
        if (path.Count == k)
        {
            result.Add(new List<int>(path));
            return;
        }

        for (int i = start; i <= n; i++)
        {
            path.Add(i);
            Recurse(i + 1, n, k, path, result);
            path.RemoveAt(path.Count - 1);
        }
    }
}

