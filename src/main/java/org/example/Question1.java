package org.example;

import java.util.ArrayList;
import java.util.List;

public class Question1 {
    // Returns all possible combinations of k numbers chosen from the range [1, n]
    public static List<List<Integer>> question1(int n, int k) {
        List<List<Integer>> ans = new ArrayList<>();
        if (k < 0 || n < 0 || k > n) return ans;
        backtrack(1, n, k, new ArrayList<>(), ans);
        return ans;
    }

    private static void backtrack(int start, int n, int k, List<Integer> path, List<List<Integer>> ans) {
        if (path.size() == k) {
            ans.add(new ArrayList<>(path));
            return;
        }
        // Prune: if remaining numbers are insufficient to fill the path
        int remaining = k - path.size();
        for (int i = start; i <= n - remaining + 1; i++) {
            path.add(i);
            backtrack(i + 1, n, k, path, ans);
            path.remove(path.size() - 1);
        }
    }
}
