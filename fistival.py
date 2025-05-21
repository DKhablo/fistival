import json
from typing import List, Dict

# Загрузка данных из файла (если есть)
def load_data() -> Dict:
    try:
        with open("festival_data.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"participants": [], "performances": [], "scores": []}

# Сохранение данных в файл
def save_data(data: Dict) -> None:
    with open("festival_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Добавление участника
def add_participant(data: Dict) -> None:
    name = input("Введите ФИО участника: ")
    group = input("Введите группу (курс/факультет): ")
    data["participants"].append({"name": name, "group": group})
    save_data(data)
    print(f"✅ Участник {name} добавлен!")

# Добавление выступления
def add_performance(data: Dict) -> None:
    if not data["participants"]:
        print("❌ Нет участников! Сначала добавьте их.")
        return
    print("\nСписок участников:")
    for i, participant in enumerate(data["participants"], 1):
        print(f"{i}. {participant['name']} ({participant['group']})")

    try:
        participant_id = int(input("\nВыберите номер участника: ")) - 1
        if participant_id < 0 or participant_id >= len(data["participants"]):
            raise ValueError
    except ValueError:
        print("❌ Неверный номер участника!")
        return

    title = input("Введите название выступления: ")
    data["performances"].append({
        "participant_id": participant_id,
        "title": title
    })
    save_data(data)
    print("✅ Выступление добавлено!")

# Добавление оценки
def add_score(data: Dict) -> None:
    if not data["performances"]:
        print("❌ Нет выступлений!")
        return

    print("\nСписок выступлений:")
    for i, perf in enumerate(data["performances"], 1):
        participant = data["participants"][perf["participant_id"]]
        print(f"{i}. {perf['title']} ({participant['name']})")

    try:
        perf_id = int(input("\nВыберите номер выступления: ")) - 1
        if perf_id < 0 or perf_id >= len(data["performances"]):
            raise ValueError
    except ValueError:
        print("❌ Неверный номер выступления!")
        return

    try:
        score = float(input("Введите оценку (1-10): "))
        if score < 1 or score > 10:
            raise ValueError
    except ValueError:
        print("❌ Оценка должна быть от 1 до 10!")
        return

    data["scores"].append({
        "performance_id": perf_id,
        "score": score
    })
    save_data(data)
    print("✅ Оценка добавлена!")

# Подведение итогов
def show_results(data: Dict) -> None:
    if not data["scores"]:
        print("❌ Нет оценок!")
        return

    # Считаем средние оценки для каждого выступления
    scores_sum = {}
    scores_count = {}

    for score in data["scores"]:
        perf_id = score["performance_id"]
        if perf_id not in scores_sum:
            scores_sum[perf_id] = 0
            scores_count[perf_id] = 0
        scores_sum[perf_id] += score["score"]
        scores_count[perf_id] += 1

    avg_scores = []
    for perf_id in scores_sum:
        avg = scores_sum[perf_id] / scores_count[perf_id]
        perf = data["performances"][perf_id]
        participant = data["participants"][perf["participant_id"]]
        avg_scores.append({
            "name": participant["name"],
            "title": perf["title"],
            "avg_score": avg
        })

    # Сортируем по убыванию оценки
    avg_scores.sort(key=lambda x: x["avg_score"], reverse=True)

    print("\n🏆 Топ-3 выступления:")
    for i, entry in enumerate(avg_scores[:3], 1):
        print(f"{i}. {entry['title']} ({entry['name']}) — {entry['avg_score']:.2f} баллов")

# Главное меню
def main():
    data = load_data()

    while True:
        print("\n🎭 Фестиваль художественной самодеятельности")
        print("1. Добавить участника")
        print("2. Добавить выступление")
        print("3. Добавить оценку")
        print("4. Показать итоги")
        print("5. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            add_participant(data)
        elif choice == "2":
            add_performance(data)
        elif choice == "3":
            add_score(data)
        elif choice == "4":
            show_results(data)
        elif choice == "5":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор!")

if __name__ == "__main__":
    main()