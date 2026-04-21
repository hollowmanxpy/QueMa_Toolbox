import os

def create_demo_files():
    # 在桌面上创建一个名为 QueMa_Demo_Project 的文件夹
    base_dir = os.path.join(os.path.expanduser("~"), "Desktop", "QueMa_Demo_Project")
    os.makedirs(base_dir, exist_ok=True)

    files_content = {
        "main.py": "def hello_python():\n    print('Hello! 这是 Python 测试文件。')",
        "App.java": "public class App {\n    public static void main(String[] args) {\n        System.out.println(\"Java 测试通过\");\n    }\n}",
        "script.js": "const greet = () => console.log('JavaScript is running');\ngreet();",
        "index.html": "<html>\n  <body>\n    <h1>HTML 测试页面</h1>\n  </body>\n</html>",
        "style.css": "body {\n  color: #333;\n  background-color: #f4f4f4;\n}",
        "logic.cpp": "#include <iostream>\n\nint main() {\n    std::cout << \"C++ 提取正常\" << std::endl;\n    return 0;\n}",
        "App.vue": "<template>\n  <div>Vue 框架测试</div>\n</template>\n<script>\nexport default {\n  name: 'App'\n}\n</script>",
        "readme.txt": "这是一个用于测试雀码提取功能的纯文本说明文件。"
    }

    for filename, content in files_content.items():
        file_path = os.path.join(base_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"🎉 测试文件夹已成功生成！\n请前往桌面查看：{base_dir}\n您可以直接将此文件夹作为代码路径进行提取测试。")

if __name__ == "__main__":
    create_demo_files()