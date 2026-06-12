# AI Coding Mentor — DSA Hint Engine

An intelligent web application that analyzes Data Structure & Algorithm (DSA) code and provides targeted hints to help developers identify and fix bugs without spoiling the solution.

## Features

- **Multi-Language Support**: Analyze code in Python, C++, Java, and JavaScript
- **AI-Powered Bug Detection**: Uses Google Gemini to identify logical bugs in DSA implementations
- **Intelligent Hints**: Generates two levels of hints (general guidance → specific debugging direction)
- **Complexity Analysis**: Reports time and space complexity of submitted solutions
- **Topic Tagging**: Automatically categorizes code by DSA topic (Arrays, Graphs, Trees, etc.)
- **User Feedback Loop**: Track which hints are most helpful via upvote/downvote mechanism
- **Progressive Disclosure**: Show Hint 2 only after user reviews Hint 1 (prevents immediate spoilers)

## Architecture

```
___________________________________________________________
|         DEVELOPMENT (Build-Time with Copilot CLI)       |
|---------------------------------------------------------|
| - Generated initial Streamlit app structure & UI layout |
| - Co-designed Gemini prompt engineering (prompts.py)    |
| - Built JSON parsing & error-handling logic (gemini.py) |
| - Debugged edge cases (fallback responses, retries)     |
| - Accelerated README & docstring generation             |
|___________________________ _____________________________|
                            |
                            | produced
                            v
____________________________v______________________________
|                  RUNTIME ARCHITECTURE                   |
|---------------------------------------------------------|
|                 Streamlit Web Interface                 |
|          (Problem + Code Input + Language)              |
|                           |                             |
|                           | analyze_code()              |
|                           v                             |
|            gemini.py (AI Analysis Engine)               |
| - Constructs system/user prompts                        |
| - Calls Google Generative AI (Gemini)                   |
| - Parses response into structured JSON                  |
|                           |                             |
|                           v                             |
|          Google Generative AI (Gemini API)              |
| - Analyzes code for bugs                                |
| - Generates teaching hints                              |
| - Evaluates complexity                                  |
|                           |                             |
|                           v                             |
|                Rendered UI Components                   |
| - Bug detection badge                                   |
| - Hints with feedback buttons                           |
| - Complexity metrics                                    |
| - Celebration animation (if correct)                    |
|_________________________________________________________|
```

## Local Setup

### Prerequisites
- Python 3.8 or higher
- Google Generative AI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Agents_League
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

The app will open at `http://localhost:8501`

## Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_generative_ai_key_here
```

**How to get your API key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key and paste into `.env`

## How GitHub Copilot Was Used

This project was developed using **GitHub Copilot CLI** for rapid prototyping and implementation:

- **Code Generation**: Copilot generated the initial Flask/Streamlit structure and API integration boilerplate
- **Prompt Engineering**: Copilot helped craft effective system prompts for the Gemini API to extract structured hints
- **Debugging**: Copilot assisted in identifying and fixing JSON parsing issues and edge cases
- **Testing**: Copilot generated test cases for multi-language support and hint quality validation
- **Documentation**: Copilot accelerated README and docstring generation

## Sample Test Cases

### Test Case 1: Two Sum
**Problem:** Find two indices of numbers in an array that add up to a target.

**Buggy Code (Python):**
```python
def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i, len(nums)):  # BUG: should be i+1
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

**Expected Hints:**
- **Hint 1:** "The inner loop starts from the same index as the outer loop. What happens if you add a number to itself?"
- **Hint 2:** "Change the inner loop to start from `i+1` to avoid pairing the same element with itself."
- **Bug Detection:** Off-by-one error in loop initialization
- **Complexity:** O(n²) time, O(1) space

---

### Test Case 2: Binary Search Off-by-One Bug
**Problem:** Find the index of a target value in a sorted array.

**Buggy Code (C++):**
```cpp
int binarySearch(vector<int>& nums, int target) {
    int left = 0, right = nums.size();  // BUG: should be nums.size() - 1
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

**Expected Hints:**
- **Hint 1:** "Your right boundary might be out of bounds. What's the last valid index in an array of size n?"
- **Hint 2:** "Change `right = nums.size()` to `right = nums.size() - 1` to stay within array bounds."
- **Bug Detection:** Array index out of bounds
- **Complexity:** O(log n) time, O(1) space

---

### Test Case 3: Sliding Window Mistake
**Problem:** Find the maximum sum of a contiguous subarray of size k.

**Buggy Code (Java):**
```java
int maxSumSubarray(int[] nums, int k) {
    int maxSum = 0, windowSum = 0;
    for (int i = 0; i < nums.length; i++) {
        windowSum += nums[i];
        if (i >= k - 1) {  // BUG: doesn't remove left element
            maxSum = Math.max(maxSum, windowSum);
        }
    }
    return maxSum;
}
```

**Expected Hints:**
- **Hint 1:** "You're adding elements to the window, but are you removing the ones that fall out of the window?"
- **Hint 2:** "Use a two-pointer approach: add `nums[i]` and remove `nums[i-k]` when the window is full."
- **Bug Detection:** Incorrect window sliding logic
- **Complexity:** O(n) time, O(1) space

## Hackathon Submission Notes

This MVP was created for a hackathon with the following goals:

- **Rapid Prototyping**: Built in minimal time using Streamlit for instant UI iteration
- **AI Integration**: Leveraged Google Generative AI (Gemini) for cost-effective code analysis
- **Teaching Focus**: Designed to support learning without giving away solutions
- **Feedback Integration**: Collected user preference data (hint helpfulness) for future model fine-tuning

**Key Decisions:**
- Used Streamlit over Flask for rapid development and hot-reload capabilities
- Chose Gemini API for balance of cost, speed, and quality
- Implemented progressive hint disclosure to encourage problem-solving
- Stored feedback data to identify high-quality hint patterns

## Future Improvements

- **Multi-Turn Conversations**: Let users ask follow-up questions about hints without re-submitting code
- **Code Visualization**: Add execution trace visualization to help understand bug origins
- **Hint Quality Tuning**: Use feedback data to fine-tune prompts and improve hint relevance
- **Complexity Validation**: Verify submitted complexity claims against code analysis
- **Leaderboard**: Track user progress and celebrate milestones
- **More Languages**: Add Rust, Go, TypeScript, and other popular DSA languages
- **Problem Database**: Integrate with LeetCode/HackerRank APIs to auto-populate problem statements
- **Caching**: Cache analyses for identical code submissions to reduce API calls
- **Peer Comparison**: Show anonymized comparison of how others solved the same problem
- **Export Hints**: Let users save hints and solutions as study notes

---

**Built with ❤️ using Streamlit, Google Gemini API, and GitHub Copilot**
