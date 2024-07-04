import json

predicted_labels =[[{'id': 0, 'start_offset': 0, 'end_offset': 2, 'label': '0'},#0
                    {'id': 1, 'start_offset': 2, 'end_offset': 4, 'label': '1'},#1
                    {'id': 2, 'start_offset': 4, 'end_offset': 8, 'label': '2'},#(2,3)
                    {'id': 3, 'start_offset': 8, 'end_offset': 12, 'label': '3'},#4,5
                    {'id': 4, 'start_offset': 12, 'end_offset': 16, 'label': '4'},#6,7
                    {'id': 5, 'start_offset': 16, 'end_offset': 20, 'label': '5'},#8

                    #20-24可变
                    {'id': 9, 'start_offset': 24, 'end_offset': 28, 'label': '9'},#12,13
                   # 28-32 （14,15)可变
                    {'id': 10, 'start_offset': 32, 'end_offset': 34, 'label': '10'},#16
                    {'id': 11, 'start_offset': 34, 'end_offset': 36, 'label': '11'},#17
                  #  36-40  （18,19）可变
                    {'id': 12, 'start_offset': 40, 'end_offset': 42, 'label': '12'}#20
# 42-48 （21-23）可变
]
]
variable_fields_rules = {
    '10|11': (20, 24),
    '14|15': (28, 32),
    '18|19': (36, 40),
    '19|20|21': (42, 48)
}



def read_labels_from_jsonl(file_path):
    labels = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line.strip())
            labels.append(data['entities'])
    return labels


def calculate_accuracy_with_variable_fields(predicted_labels, true_labels, variable_fields_rules):
    matched_count = 0

    # 将预测标签和真实标签转换为以偏移量为基准的形式
    predicted_offsets = [(label['start_offset'], label['end_offset']) for label in predicted_labels[0]]
    true_offsets = [(label['start_offset'], label['end_offset']) for label in true_labels[0]]

    for pred_offset in predicted_offsets:
        # 检查预测偏移量是否直接匹配真实偏移量
        if pred_offset in true_offsets:
            matched_count += 1
        else:
            # 对于不直接匹配的情况，检查是否符合可变字段的规则
            for variable_rule in variable_fields_rules.values():
                start_range, end_range = variable_rule
                if start_range <= pred_offset[0] and end_range >= pred_offset[1]:
                    matched_count += 1
                    break

    accuracy = matched_count / len(predicted_labels[0])
    return accuracy
true_labels = read_labels_from_jsonl('labeled_data.jsonl')  # 从文件读取的真实标签

accuracy = calculate_accuracy_with_variable_fields(predicted_labels, true_labels, variable_fields_rules)
print(f"Accuracy considering variable fields: {accuracy:.4f}")