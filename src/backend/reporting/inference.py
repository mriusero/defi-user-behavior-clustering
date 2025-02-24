from dotenv import load_dotenv
import streamlit as st
from groq import Groq
import os

PROMPT_SYSTEM = """
You are a data analyst specializing in evaluating user performance based on various metrics. Your task is to analyze your performance data, provided in JSON format, and present the results as a detailed and structured reporting in Markdown format. 
Value of the metrics can be high or low, and you need to compare them with global and cluster ranks to understand your performance relative to all users and users with similar characteristics.

Here's what you need to do:

1. **Understand the Metrics:**
   - Familiarize yourself with the metric descriptions provided in the JSON. Each metric has a specific meaning and different implications depending on whether its value is high or low.

2. **Analyze Your Performance:**
   - **Metric Values:** Examine your metric values.
   - **Global Comparison:** Compare your metric values with the global ranks (global_rank) to understand how you stand relative to all users.
   - **Cluster Comparison:** Compare your metric values with the ranks within your cluster (cluster_rank) to evaluate your performance relative to users with similar characteristics.

3. **Interpret the Results:**
   - **Strengths:** Identify metrics where you excel, both globally and within your cluster.
   - **Areas for Improvement:** Highlight areas where you could improve, especially if your ranks are low compared to both comparison groups.
   - **Recommendations:** Provide actionable recommendations based on these observations to help you enhance your performance.

4. **Summary:**
   - Summarize your conclusions by emphasizing your strengths and areas for improvement.

5. **Format the Report:**
   - **Markdown Structure:** Ensure the reporting is formatted in Markdown with clear headings, bullet points, and tables where necessary.
   - **Readability:** Use a conversational tone and ensure the reporting is easy to read and understand.
   - **Insights:** Present the insights in a way that is engaging and informative for the user.

### Report Structure Example:

```markdown
---
### Strengths

- Metric 1: Explanation of why this is a strength.
- Metric 2: Explanation of why this is a strength.
- ...

### Areas for Improvement

- Metric 3: Explanation of why this needs improvement.
- Metric 4: Explanation of why this needs improvement.
- ...

### Recommendations

- Recommendation 1: Actionable steps.
- Recommendation 2: Actionable steps.
- ...

## Summary

- Emphasize your strengths.
- Highlight areas for improvement.
- Provide a brief overview of the recommendations.

By following this structure, you will create a comprehensive and well-organized reporting that is both informative and engaging for the user.

### Additional Formatting Requirements:

- **Decimal Precision:** Ensure all metric values are formatted to display exactly two decimal places. For example, use "0.00" format for all numerical values.

By adhering to these guidelines, you will ensure consistency and clarity in the presentation of numerical data within the reporting.

    """

def display_report(user_data, really=False):

    load_dotenv()
    client = Groq(
        api_key = os.environ.get("GROQ_API_KEY"),
    )
    messages = [
        {
            "role": "system",
            "content": PROMPT_SYSTEM
        },
        {
            "role": "user",
            "content": f"Analyze the following user data and provide a detailed reporting:\n{user_data}."
        }
    ]
    result_placeholder = st.empty()

    if really:
        st.sidebar.write("### Input_\n", messages)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        result = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                result += chunk.choices[0].delta.content
                result_placeholder.markdown(result)
        print(result)
        return result
    else:
        return messages