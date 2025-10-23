using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NssfTechInterview.BusinessLogic
{
    public class BusinessLogic
    {

        /// <summary>
        /// Generates all possible combinations of k numbers from 1 to n.
        /// </summary>
        /// <param name="n">The upper limit of the number range.</param>
        /// <param name="k">The number of elements in each combination.</param>
        /// <returns>A list of combinations, where each combination is a list of integers.</returns>
        public IList<IList<int>> GetCombinations(int n, int k)
        {
            // Result list to store all combinations
            IList<IList<int>> result = new List<IList<int>>();

            // Start backtracking from number 1 with an empty combination
            Backtrack(result, new List<int>(), 1, n, k);
 
            return result;
        }

        /// <summary>
        /// Helper function that uses backtracking to generate combinations.
        /// </summary>
        /// <param name="result">The main result list to store valid combinations.</param>
        /// <param name="tempList">Current combination being built.</param>
        /// <param name="start">The starting number for the current recursion level.</param>
        /// <param name="n">The upper limit of the number range.</param>
        /// <param name="k">The number of elements in each combination.</param>
        private void Backtrack(IList<IList<int>> result, List<int> tempList, int start, int n, int k)
        {
            // If the current combination has reached size k, add a copy to the result
            if (tempList.Count == k)
            {
                result.Add(new List<int>(tempList)); // Add a new list to avoid reference issues
                return; // Stop further recursion for this branch
            }

            // Loop from the current starting number to n
            for (int i = start; i <= n; i++)
            {
                tempList.Add(i); // Choose the current number i
                Backtrack(result, tempList, i + 1, n, k); // Recurse with next starting number
                tempList.RemoveAt(tempList.Count - 1); // Undo the choice (backtrack) to try next number
            }
        }
    }
}
