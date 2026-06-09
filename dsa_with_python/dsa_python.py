import streamlit as st
import google.generativeai as genai
import json
import time
from typing import List, Dict

# Configure the Streamlit app
st.set_page_config(
    page_title="DSA Master with Gemini AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("⚡ DSA Master with Gemini AI")
st.markdown("""
**From Zero to Advanced** - Complete Data Structures & Algorithms learning with Python  
Get questions, algorithms, code, and explanations for all DSA topics.
""")

# Sidebar for API key input and topic selection
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    
    st.header("Topics")
    selected_category = st.selectbox(
        "Select Category",
        [
            "Python Fundamentals",
            "DSA Core Concepts",
            "Arrays/Lists",
            "Strings",
            "Recursion & Backtracking",
            "Linked List",
            "Stack & Queue",
            "Trees",
            "Graphs",
            "Dynamic Programming",
            "Advanced Topics",
            "Extras for Google-level Interviews"
        ]
    )
    
    # Topic mapping based on categories
    TOPICS = {
        "Python Fundamentals": [
            "Variables & Data Types", "Input / Output", "Operators", 
            "Conditional Statements", "Loops", "Functions", 
            "Strings", "Lists, Tuples, Sets, Dictionaries", 
            "Exception Handling", "File Handling"
        ],
        "DSA Core Concepts": [
            "Complexity Analysis", "Time vs Space Trade-offs"
        ],
        "Arrays/Lists": [
            "Traversal, Insertion, Deletion", "Searching", "Sorting", 
            "Prefix Sum", "Sliding Window", "Two Pointer Technique",
            "Kadane's Algorithm", "Matrix Problems"
        ],
        "Strings": [
            "Palindrome Check", "Anagram Check", "Substring Search",
            "String Hashing", "Longest Substring Problems"
        ],
        "Recursion & Backtracking": [
            "Factorial, Fibonacci", "Tower of Hanoi", "Subsets/Power Set",
            "Permutations & Combinations", "Rat in a Maze", 
            "N-Queens Problem", "Sudoku Solver"
        ],
        "Linked List": [
            "Singly Linked List", "Doubly Linked List", "Circular Linked List",
            "Reverse a Linked List", "Find Middle Element", 
            "Detect Cycle", "Merge Two Sorted Lists"
        ],
        "Stack & Queue": [
            "Stack using List/Deque", "Queue using List/Deque", 
            "Circular Queue", "Priority Queue", "Applications"
        ],
        "Trees": [
            "Binary Tree Basics", "Tree Traversals", "Height & Diameter",
            "Binary Search Tree", "Lowest Common Ancestor", 
            "Balanced BST", "Trie"
        ],
        "Graphs": [
            "Graph Representation", "DFS", "BFS", "Dijkstra's Algorithm",
            "Bellman-Ford Algorithm", "Floyd-Warshall Algorithm",
            "Minimum Spanning Tree", "Topological Sort", "Union-Find",
            "Detect Cycle in Graph", "Bipartite Graph Check"
        ],
        "Dynamic Programming": [
            "Fibonacci", "Longest Common Subsequence", 
            "Longest Increasing Subsequence", "Knapsack Problems",
            "Matrix Chain Multiplication", "DP on Grid", 
            "DP on Strings", "DP on Subsets", "Coin Change Problems",
            "Catalan Numbers"
        ],
        "Advanced Topics": [
            "Heap & Heap Sort", "Priority Queue Applications",
            "Segment Tree", "Fenwick Tree", "Bit Manipulation Tricks",
            "Disjoint Set Union"
        ],
        "Extras for Google-level Interviews": [
            "Greedy Algorithms", "Divide & Conquer", 
            "Mathematical Algorithms", "System Design Basics"
        ]
    }
    
    selected_topic = st.selectbox("Select Topic", TOPICS[selected_category])
    
    difficulty = st.radio(
        "Select Difficulty Level",
        ["All Levels", "Easy", "Medium", "Hard"],
        index=0
    )
    
    generate_btn = st.button("Generate Content")

# Initialize Gemini model
def initialize_model(api_key: str):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
        return None
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        return model
    except Exception as e:
        st.error(f"Error initializing Gemini model: {str(e)}")
        return None

# Generate content for the selected topic
def generate_topic_content(model, topic: str, difficulty: str = "All Levels") -> Dict:
    prompt = f"""
    You are an expert Data Structures and Algorithms instructor teaching with Python. 
    The student wants to learn about: {topic}.
    
    Provide a comprehensive learning experience with the following structure:
    
    1. **Understanding the Topic**: Explain what {topic} is in simple terms with 2-3 examples.
    2. **Questions**:
       - 5 Easy level questions with examples
       - 5 Medium level questions with examples
       - 5 Hard level questions with examples
    3. **Algorithm Walkthrough**: For each difficulty level, pick one question and:
       a. Explain the problem statement clearly
       b. Provide step-by-step algorithm
       c. Show Python code implementation
       d. Explain the code in detail
       e. Analyze time and space complexity
    
    Format the output as a JSON object with these keys:
    - "topic_explanation"
    - "easy_questions"
    - "medium_questions"
    - "hard_questions"
    - "easy_algorithm" (containing problem, algorithm, code, explanation, complexity)
    - "medium_algorithm" (same structure as easy_algorithm)
    - "hard_algorithm" (same structure as easy_algorithm)
    
    Make sure all code is properly formatted and explained for a beginner to understand.
    """
    
    try:
        response = model.generate_content(prompt)
        if response.text:
            try:
                # Try to parse the JSON directly
                return json.loads(response.text)
            except json.JSONDecodeError:
                # Sometimes Gemini adds markdown, try to extract JSON
                json_str = response.text.strip('```json\n').strip('\n```')
                return json.loads(json_str)
        else:
            st.error("No response text from Gemini")
            return None
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return None

# Display the generated content
def display_content(content: Dict, difficulty: str):
    if not content:
        st.error("No content generated")
        return
    
    st.header(content.get('topic_name', selected_topic))
    
    with st.expander("📚 Topic Explanation"):
        st.write(content.get('topic_explanation', 'No explanation provided.'))
    
    # Questions section
    st.subheader("📝 Questions")
    
    if difficulty in ["All Levels", "Easy"]:
        with st.expander("Easy Questions"):
            for i, q in enumerate(content.get('easy_questions', []), 1):
                st.markdown(f"{i}. {q}")
    
    if difficulty in ["All Levels", "Medium"]:
        with st.expander("Medium Questions"):
            for i, q in enumerate(content.get('medium_questions', []), 1):
                st.markdown(f"{i}. {q}")
    
    if difficulty in ["All Levels", "Hard"]:
        with st.expander("Hard Questions"):
            for i, q in enumerate(content.get('hard_questions', []), 1):
                st.markdown(f"{i}. {q}")
    
    # Algorithm walkthroughs
    st.subheader("🔍 Detailed Algorithm Walkthroughs")
    
    if difficulty in ["All Levels", "Easy"] and 'easy_algorithm' in content:
        with st.expander("Easy Level Walkthrough"):
            algo = content['easy_algorithm']
            st.markdown("**Problem:** " + algo.get('problem', ''))
            st.markdown("**Algorithm Steps:**")
            st.write(algo.get('algorithm', ''))
            st.markdown("**Python Code:**")
            st.code(algo.get('code', ''), language='python')
            st.markdown("**Explanation:**")
            st.write(algo.get('explanation', ''))
            st.markdown("**Complexity Analysis:**")
            st.write(algo.get('complexity', ''))
    
    if difficulty in ["All Levels", "Medium"] and 'medium_algorithm' in content:
        with st.expander("Medium Level Walkthrough"):
            algo = content['medium_algorithm']
            st.markdown("**Problem:** " + algo.get('problem', ''))
            st.markdown("**Algorithm Steps:**")
            st.write(algo.get('algorithm', ''))
            st.markdown("**Python Code:**")
            st.code(algo.get('code', ''), language='python')
            st.markdown("**Explanation:**")
            st.write(algo.get('explanation', ''))
            st.markdown("**Complexity Analysis:**")
            st.write(algo.get('complexity', ''))
    
    if difficulty in ["All Levels", "Hard"] and 'hard_algorithm' in content:
        with st.expander("Hard Level Walkthrough"):
            algo = content['hard_algorithm']
            st.markdown("**Problem:** " + algo.get('problem', ''))
            st.markdown("**Algorithm Steps:**")
            st.write(algo.get('algorithm', ''))
            st.markdown("**Python Code:**")
            st.code(algo.get('code', ''), language='python')
            st.markdown("**Explanation:**")
            st.write(algo.get('explanation', ''))
            st.markdown("**Complexity Analysis:**")
            st.write(algo.get('complexity', ''))

# Main app logic
if generate_btn and api_key:
    with st.spinner("Generating content with Gemini AI..."):
        model = initialize_model(api_key)
        if model:
            content = generate_topic_content(model, selected_topic, difficulty)
            if content:
                # Add topic name to content for display
                content['topic_name'] = selected_topic
                display_content(content, difficulty)
else:
    st.info("Please select a topic and click 'Generate Content' to begin.")

# Add some tips and information
st.sidebar.markdown("""
### Tips:
1. Enter your Gemini API key to use the app
2. Select a DSA category and specific topic
3. Choose difficulty level or keep 'All Levels'
4. Click 'Generate Content' to get questions and explanations

### Features:
- Complete DSA coverage (82 topics)
- Questions at 3 difficulty levels
- Detailed algorithm walkthroughs
- Python code examples
- Complexity analysis
""")