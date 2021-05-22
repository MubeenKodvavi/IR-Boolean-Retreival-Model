"""
Code by Mubeen Kodvavi
18K-1198 FAST NUCES
"""

import tkinter as tk
from query_processing import process_query

def run_query(event=None):
    """
    Takes user input from query box and calls query processing function.
    Results are inserted in the result box
    """
    result_box.configure(state='normal')
    result_box.delete(0.0, 'end')
    query = query_box.get()
    result = process_query(query)
    if result == 'NF':
        # files not present. Must run scripts to make index first.
        output_string = 'Please form inverted and positional index first. No file found.'
    else:
        output_string = "Documents retreived: " + str(
            len(result)) + "\nDocument IDs: " + str(result)
    result_box.insert('insert', output_string)
    result_box.configure(state='disabled')


if __name__ == '__main__':
    """All the GUI objects initialized"""
    # initializing window
    root = tk.Tk()
    root.geometry("600x300")
    root.title('Boolean Retreival Model')

    # Title Label
    tk.Label(root, text="Boolean Retreival Model",
             font=("Helvetica", 18)).pack(pady=(2, 10))

    # Label asking to enter query
    tk.Label(root, text="Enter your query",
             font=("Helvetica", 11)).pack(pady=(10, 2))

    # Text Entry Box
    query_box = tk.Entry(root, font=("Helvetica", 11), width=45)
    query_box.pack()

    # Query Submission Button that runs query
    query_button = tk.Button(root, text="SUBMIT", width=40, command=run_query).pack()

    # Label , heading for results section
    tk.Label(root, text="Results", font=("Helvetica", 11)).pack(pady=(10, 2))

    # if enter pressed run_query method called
    root.bind('<Return>', run_query)

    # resultBox
    result_box = tk.Text(root,
                         width=50,
                         height=5,
                         font=("Helvetica", 11),
                         wrap='word')
    result_box.configure(state='disabled')
    result_box.pack(pady=(0, 10))

    # window loop to monitor and render changes
    root.mainloop()