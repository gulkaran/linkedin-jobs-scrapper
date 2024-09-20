import sys
import os
import subprocess
from pathlib import Path

def customize_and_compile_latex(company_name):
    # Path to the original LaTeX template
    template_path = Path.home() / "Downloads" / "cover_letter" / "cover.tex"
    
    # Path to save the customized LaTeX file
    temp_tex_path = Path.home() / "Downloads" / "cover_letter" / "saves" / f"cover_letter_{company_name.replace(' ', '_')}.tex"
    
    # Read the LaTeX template
    with open(template_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace the company variable with the provided company name
    customized_content = content.replace(r'\newcommand{\company}{COMPANY}', f'\\newcommand{{\\company}}{{{company_name}}}')
    
    # Save the customized LaTeX file
    with open(temp_tex_path, 'w', encoding='utf-8') as file:
        file.write(customized_content)
    
    # Compile the LaTeX file to PDF
    try:
        subprocess.run(['xelatex', '-output-directory', str(temp_tex_path.parent), str(temp_tex_path)], check=True)
        print(f"Customized cover letter for {company_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling LaTeX: {e}")
    except FileNotFoundError:
        print("Error: pdflatex not found. Make sure LaTeX is installed and in your system PATH.")
    
    # Clean up temporary files
    for ext in ['.aux', '.log', '.out']:
        temp_file = temp_tex_path.with_suffix(ext)
        if temp_file.exists():
            temp_file.unlink()
    
    # Remove the temporary .tex file
    temp_tex_path.unlink()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cover_letter_customizer.py 'Company Name'")
        sys.exit(1)
    
    company_name = sys.argv[1]
    customize_and_compile_latex(company_name)
