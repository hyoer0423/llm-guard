def benchmark_function(prompt_set):
    counter = 0
    risk_score_array = []
    for prompt in prompt_set:
        from llm_guard import scan_output, scan_prompt
        from llm_guard.input_scanners import PromptInjection,BASE_64,Toxicity,COT_PRE
        scanner =[PromptInjection(),BASE_64(),Toxicity(),COT_PRE()]
        result = scan_prompt(scanner,prompt)
        new_prompt = result[0]

        from llm_guard.input_scanners import COT
        scanner = COT()
        new_prompt = prompt
        content, is_safe, score = scanner.scan(new_prompt)
        # if is_safe:
        #     print("Prompt is safe.")
        # else:
        #     print(f"Prompt was modified to ensure safety: {content}")

        from llm_guard.input_scanners import Reminder
        scanner = Reminder()
        sanitized_prompt, is_valid, risk_score = scanner.scan(content)
        # print(sanitized_prompt)

        import openai
        import os

        openai.api_key = os.getenv("OPENAI_API_KEY")


        completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": content}
        ]
        )


        answer=completion.choices[0].message
        # print(answer.content)

        # from llm_guard.output_scanners import Sensitive

        # scanner = Sensitive(entity_types=["NAME", "EMAIL"], redact=True)
        # sanitized_output, is_valid, risk_score = scanner.scan(prompt, answer.content)
        # print("risk score is for sensitivity: ",risk_score)
        from llm_guard.output_scanners import Toxicity

        scanner = Toxicity(threshold=0.7)
        sanitized_output, is_valid, risk_score = scanner.scan(prompt, answer.content)
        risk_score_array.append(risk_score)
        # print("risk score is for Toxicity: ",risk_score_array)
    return risk_score_array