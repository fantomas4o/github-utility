# Author     : Fedya Serafiev
# Version    : 1.2
# License    : MIT
# Copyright  : Fedya Serafiev (2023)
# Github     : https://github.com/fantomas4o/github-utility
# Contact    : https://urocibg.eu

import os
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from github import Github, GithubException

class GitHubApp:
    def __init__(self, master):
        self.master = master
        self.master.title("GitHub Utility")
        
        style = ttk.Style()
        style.configure('TLabel', font=('Verdana', 14))
        style.configure('TEntry', font=('Verdana', 14))
        style.configure('TRadiobutton', font=('Verdana', 14))
        style.configure('TButton', font=('Verdana', 14))

        ttk.Label(self.master, text="GitHub Token:").grid(row=0, column=0)
        self.token_entry = ttk.Entry(self.master)
        self.token_entry.grid(row=0, column=1)

        ttk.Label(self.master, text="Repo Name:").grid(row=1, column=0)
        self.repo_name_entry = ttk.Entry(self.master)
        self.repo_name_entry.grid(row=1, column=1)

        self.action_var = tk.StringVar()
        self.action_var.set("upload")

        ttk.Radiobutton(self.master, text="Upload", variable=self.action_var, value="upload").grid(row=2, column=0)
        ttk.Radiobutton(self.master, text="Clone", variable=self.action_var, value="clone").grid(row=2, column=1)

        self.file_paths = []
        self.add_file_button = ttk.Button(self.master, text="Add File", command=self.add_file)
        self.add_file_button.grid(row=3, column=0)

        self.commit_message_entry = ttk.Entry(self.master)
        self.commit_message_entry.grid(row=4, column=1)
        ttk.Label(self.master, text="Commit Message:").grid(row=4, column=0)

        self.submit_button = ttk.Button(self.master, text="Submit", command=self.submit)
        self.submit_button.grid(row=5, columnspan=2)

        self.output_text = tk.Text(self.master, wrap="word", width=40, height=10, font=('Verdana', 14))
        self.output_text.grid(row=6, columnspan=2)

    def print_to_text_widget(self, message):
        self.output_text.insert(tk.END, message + '\n')

    def add_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_paths.append(file_path)

    def submit(self):
        token = self.token_entry.get()
        repo_name = self.repo_name_entry.get()
        commit_message = self.commit_message_entry.get()
        action = self.action_var.get()

        if action == "upload":
            self.upload_to_github(token, repo_name, self.file_paths, commit_message)
        elif action == "clone":
            self.clone_repo(token, repo_name)

    def upload_to_github(self, token, repo_name, file_paths, commit_message):
        g = Github(token)
        user = g.get_user()
        try:
            repo = user.create_repo(repo_name)
            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    content = file.read()
                file_name = os.path.basename(file_path)
                repo.create_file(file_name, commit_message, content)
            self.print_to_text_widget(f"Files have been successfully uploaded to the repository '{repo_name}'.")
        except GithubException as e:
            self.print_to_text_widget(f"An error occurred while uploading the files: {e}")

    def clone_repo(self, token, repo_name):
        try:
            g = Github(token)
            user = g.get_user()
            username = user.login
            command = f"git clone https://{token}@github.com/{username}/{repo_name}.git"
            subprocess.run(command, shell=True, check=True)
            self.print_to_text_widget(f"Repository '{repo_name}' has been successfully cloned.")
        except subprocess.CalledProcessError as e:
            self.print_to_text_widget(f"An error occurred while cloning the repository: {e}")
        except GithubException as e:
            self.print_to_text_widget(f"An error occurred while accessing GitHub: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubApp(root)
    root.mainloop()
