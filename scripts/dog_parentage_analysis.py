#!/usr/bin/env python3
"""
Dog DNA Parentage Analysis Script

This script analyzes DNA profiles from ISAG format Excel files to determine parentage.
It should be run from the 'scripts' folder with DNA files in the 'data' folder.

Folder structure:
project/
├── scripts/
│   └── dog_parentage_analysis.py  (this file)
└── data/
    ├── Father.xlsx
    ├── Mother.xlsx
    └── Offspring.xlsx

Usage:
    python dog_parentage_analysis.py
"""

import pandas as pd
import numpy as np
from collections import defaultdict, Counter
import openpyxl
from pathlib import Path
import os
import sys

class DogDNAParentageAnalyzer:
    def __init__(self):
        self.profiles = {}
        self.analysis_results = {}
        
    def load_dog_profile(self, excel_file, dog_name, profile_type="DNA Page 3"):
        """
        Load a dog's DNA profile from Excel file
        
        Parameters:
        excel_file: path to Excel file
        dog_name: identifier for this dog (e.g., 'Mother', 'Father', 'Offspring')
        profile_type: which sheet to use ('DNA Page 1', 'DNA Page 2', or 'DNA Page 3')
        """
        try:
            # Check if file exists
            if not os.path.exists(excel_file):
                print(f"Error: File not found: {excel_file}")
                return False
                
            # Load the specified DNA page
            df = pd.read_excel(excel_file, sheet_name=profile_type, header=None)
            
            # Set column names based on the structure we observed
            if profile_type == "DNA Page 3":
                # DNA Page 3 has MarkerID, empty column, Genotype
                df.columns = ['MarkerID', 'Location', 'Genotype']
            else:
                # DNA Page 1 & 2 have MarkerID, Location, Genotype
                df.columns = ['MarkerID', 'Location', 'Genotype']
            
            # Clean up the data
            df = df.dropna(subset=['MarkerID', 'Genotype'])
            df = df[df['MarkerID'] != '']
            df = df[df['Genotype'] != '']
            
            # Store the profile
            self.profiles[dog_name] = {
                'data': df,
                'file': excel_file,
                'profile_type': profile_type,
                'marker_count': len(df)
            }
            
            print(f"Loaded {dog_name}: {len(df)} markers from {profile_type}")
            return True
            
        except Exception as e:
            print(f"Error loading {dog_name} from {excel_file}: {str(e)}")
            return False
    
    def parse_genotype(self, genotype_str):
        """Parse genotype string to extract alleles"""
        if pd.isna(genotype_str) or genotype_str == '':
            return None
        
        genotype_str = str(genotype_str).strip()
        
        # Handle different formats
        if '/' in genotype_str:
            alleles = genotype_str.split('/')
        elif '|' in genotype_str:
            alleles = genotype_str.split('|')
        else:
            # Assume homozygous if no separator
            alleles = [genotype_str, genotype_str]
        
        return sorted([allele.strip() for allele in alleles])
    
    def check_mendelian_inheritance(self, parent1_genotype, parent2_genotype, offspring_genotype):
        """Check if offspring genotype follows Mendelian inheritance"""
        if not all([parent1_genotype, parent2_genotype, offspring_genotype]):
            return False, "Missing genotype data"
        
        # Get all possible offspring genotypes
        possible_offspring = []
        for p1_allele in parent1_genotype:
            for p2_allele in parent2_genotype:
                possible_offspring.append(sorted([p1_allele, p2_allele]))
        
        # Check if actual offspring matches any possibility
        offspring_sorted = sorted(offspring_genotype)
        is_consistent = offspring_sorted in possible_offspring
        
        expected = set(tuple(x) for x in possible_offspring)
        actual = tuple(offspring_sorted)
        
        return is_consistent, f"Expected: {expected}, Got: {actual}"
    
    def analyze_parentage(self, mother_name, father_name, offspring_name):
        """
        Perform comprehensive parentage analysis
        """
        print("-"*80)
        print("DOG DNA PARENTAGE ANALYSIS")
        print("-"*80)
        
        # Check if all dogs are loaded
        missing_dogs = []
        for dog in [mother_name, father_name, offspring_name]:
            if dog not in self.profiles:
                missing_dogs.append(dog)
        
        if missing_dogs:
            print(f"Missing dog profiles: {', '.join(missing_dogs)}")
            print("Please load all dog profiles first using load_dog_profile()")
            return None
        
        mother_data = self.profiles[mother_name]['data']
        father_data = self.profiles[father_name]['data']
        offspring_data = self.profiles[offspring_name]['data']
        
        print(f"Analyzing: {mother_name} + {father_name} → {offspring_name}")
        print(f"Markers available:")
        print(f"   {mother_name}: {len(mother_data)} markers")
        print(f"   {father_name}: {len(father_data)} markers")
        print(f"   {offspring_name}: {len(offspring_data)} markers")
        
        # Find common markers across all three dogs
        mother_markers = set(mother_data['MarkerID'].values)
        father_markers = set(father_data['MarkerID'].values)
        offspring_markers = set(offspring_data['MarkerID'].values)
        
        common_markers = mother_markers & father_markers & offspring_markers
        
        print(f"Common markers for analysis: {len(common_markers)}")
        
        if len(common_markers) < 10:
            print("WARNING: Very few common markers found!")
            print("This may indicate different profile types or data quality issues.")
        
        # Perform analysis on common markers
        results = {
            'total_common_markers': len(common_markers),
            'testable_markers': 0,
            'consistent_markers': 0,
            'inconsistent_markers': 0,
            'exclusions': [],
            'marker_details': [],
            'confidence_level': 'Unknown'
        }
        
        # Create lookup dictionaries for faster access
        mother_lookup = mother_data.set_index('MarkerID')['Genotype'].to_dict()
        father_lookup = father_data.set_index('MarkerID')['Genotype'].to_dict()
        offspring_lookup = offspring_data.set_index('MarkerID')['Genotype'].to_dict()
        
        print(f"\nAnalyzing {len(common_markers)} common markers...")
        
        for marker_id in sorted(common_markers):
            mother_geno = self.parse_genotype(mother_lookup[marker_id])
            father_geno = self.parse_genotype(father_lookup[marker_id])
            offspring_geno = self.parse_genotype(offspring_lookup[marker_id])
            
            # Skip if any genotype is missing or invalid
            if not all([mother_geno, father_geno, offspring_geno]):
                continue
            
            results['testable_markers'] += 1
            
            # Check Mendelian inheritance
            is_consistent, details = self.check_mendelian_inheritance(
                mother_geno, father_geno, offspring_geno
            )
            
            marker_result = {
                'marker': marker_id,
                'mother': mother_geno,
                'father': father_geno,
                'offspring': offspring_geno,
                'consistent': is_consistent,
                'details': details
            }
            
            results['marker_details'].append(marker_result)
            
            if is_consistent:
                results['consistent_markers'] += 1
            else:
                results['inconsistent_markers'] += 1
                results['exclusions'].append(marker_result)
        
        # Calculate statistics
        if results['testable_markers'] > 0:
            consistency_rate = (results['consistent_markers'] / results['testable_markers']) * 100
            results['consistency_rate'] = consistency_rate
        else:
            results['consistency_rate'] = 0
        
        # Determine confidence level
        if results['inconsistent_markers'] == 0 and results['consistent_markers'] >= 20:
            results['confidence_level'] = 'Very High'
        elif results['inconsistent_markers'] <= 1 and results['consistent_markers'] >= 15:
            results['confidence_level'] = 'High'
        elif results['inconsistent_markers'] <= 2 and results['consistent_markers'] >= 10:
            results['confidence_level'] = 'Moderate'
        else:
            results['confidence_level'] = 'Low'
        
        # Print results
        print(f"\nANALYSIS RESULTS:")
        print(f"   Total common markers: {results['total_common_markers']}")
        print(f"   Testable markers: {results['testable_markers']}")
        print(f"   Consistent with parentage: {results['consistent_markers']}")
        print(f"   Inconsistent (exclusions): {results['inconsistent_markers']}")
        print(f"   Consistency rate: {results['consistency_rate']:.1f}%")
        print(f"   Confidence level: {results['confidence_level']}")
        
        print(f"\nPARENTAGE CONCLUSION:")
        print("-" * 50)
        
        # Determine final conclusion
        if results['inconsistent_markers'] == 0 and results['consistent_markers'] >= 15:
            conclusion = "PARENTAGE CONFIRMED"
            explanation = f"All {results['consistent_markers']} tested markers support the proposed parentage."
        elif results['inconsistent_markers'] <= 2 and results['consistent_markers'] >= 10:
            conclusion = "PARENTAGE LIKELY"
            explanation = f"Only {results['inconsistent_markers']} exclusions found among {results['testable_markers']} markers."
        elif results['inconsistent_markers'] > results['consistent_markers']:
            conclusion = "PARENTAGE EXCLUDED" 
            explanation = f"Too many exclusions ({results['inconsistent_markers']}) relative to consistent markers ({results['consistent_markers']})."
        else:
            conclusion = "INCONCLUSIVE"
            explanation = "Results are ambiguous. Additional testing may be needed."
        
        print(conclusion)
        print(explanation)
        
        # Show exclusions if any
        if results['exclusions']:
            print(f"\nEXCLUSION DETAILS ({len(results['exclusions'])} markers):")
            print("-" * 50)
            for i, exclusion in enumerate(results['exclusions'][:5], 1):  # Show first 5
                print(f"{i}. Marker {exclusion['marker']}:")
                print(f"   Mother: {exclusion['mother']}")
                print(f"   Father: {exclusion['father']}")
                print(f"   Offspring: {exclusion['offspring']}")
                print(f"   Issue: {exclusion['details']}")
                print()
            
            if len(results['exclusions']) > 5:
                print(f"   ... and {len(results['exclusions']) - 5} more exclusions")
        
        self.analysis_results = results
        return results
    
    def export_detailed_report(self, output_file="parentage_analysis_report.xlsx"):
        """Export detailed analysis report to Excel"""
        if not self.analysis_results:
            print("No analysis results to export. Run analyze_parentage() first.")
            return
        
        # Make sure output directory exists
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Summary sheet
                summary_data = {
                    'Metric': [
                        'Total Common Markers',
                        'Testable Markers', 
                        'Consistent Markers',
                        'Inconsistent Markers',
                        'Consistency Rate (%)',
                        'Confidence Level'
                    ],
                    'Value': [
                        self.analysis_results['total_common_markers'],
                        self.analysis_results['testable_markers'],
                        self.analysis_results['consistent_markers'],
                        self.analysis_results['inconsistent_markers'],
                        f"{self.analysis_results['consistency_rate']:.1f}%",
                        self.analysis_results['confidence_level']
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Detailed marker results
                if self.analysis_results['marker_details']:
                    marker_data = []
                    for marker in self.analysis_results['marker_details']:
                        marker_data.append({
                            'Marker_ID': marker['marker'],
                            'Mother_Genotype': '/'.join(marker['mother']),
                            'Father_Genotype': '/'.join(marker['father']),
                            'Offspring_Genotype': '/'.join(marker['offspring']),
                            'Consistent': marker['consistent'],
                            'Details': marker['details']
                        })
                    
                    markers_df = pd.DataFrame(marker_data)
                    markers_df.to_excel(writer, sheet_name='Marker_Details', index=False)
                
                # Exclusions only
                if self.analysis_results['exclusions']:
                    exclusion_data = []
                    for exclusion in self.analysis_results['exclusions']:
                        exclusion_data.append({
                            'Marker_ID': exclusion['marker'],
                            'Mother_Genotype': '/'.join(exclusion['mother']),
                            'Father_Genotype': '/'.join(exclusion['father']),
                            'Offspring_Genotype': '/'.join(exclusion['offspring']),
                            'Issue': exclusion['details']
                        })
                    
                    exclusions_df = pd.DataFrame(exclusion_data)
                    exclusions_df.to_excel(writer, sheet_name='Exclusions', index=False)
            
            print(f"Detailed report exported to: {output_file}")
            
        except Exception as e:
            print(f"Error exporting report: {str(e)}")


def get_file_paths():
    """Get the correct file paths based on current script location"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Go up one level to get the project root, then into data folder
    data_dir = script_dir.parent / "data"
    results_dir = script_dir.parent / "truth"
    
    # Create results directory if it doesn't exist
    results_dir.mkdir(exist_ok=True)
    
    # Define file paths
    files = {
        'mother': data_dir / "Mother.xlsx",
        'father': data_dir / "Father.xlsx", 
        'Offspring': data_dir / "Offspring.xlsx",
        'results': results_dir / "parentage_analysis_results.xlsx"
    }
    
    return files


def check_files_exist(files):
    """Check if all required files exist"""
    missing_files = []
    for name, file_path in files.items():
        if name != 'results' and not file_path.exists():
            missing_files.append(str(file_path))
    
    if missing_files:
        print("Missing required files:")
        for file in missing_files:
            print(f"   {file}")
        print("\nPlease ensure you have the following files in the data folder:")
        print("  - Mother.xlsx")
        print("  - Father.xlsx") 
        print("  - Offspring.xlsx")
        return False
    
    return True


def main():
    """Main function to run the parentage analysis"""
    print("Dog DNA Parentage Analysis")
    print("=" * 50)
    
    # Get file paths
    files = get_file_paths()
    
    print(f"Looking for files in: {files['mother'].parent}")
    print(f"Results will be saved to: {files['results']}")
    print()
    
    # Check if files exist
    if not check_files_exist(files):
        return
    
    # Initialize the analyzer
    print("Initializing DNA analyzer...")
    analyzer = DogDNAParentageAnalyzer()
    print()
    
    # Load each dog's profile
    print("Loading dog profiles...")
    success_count = 0
    
    success_count += analyzer.load_dog_profile(str(files['mother']), 'Mother', 'DNA Page 3')
    success_count += analyzer.load_dog_profile(str(files['father']), 'Father', 'DNA Page 3')
    success_count += analyzer.load_dog_profile(str(files['Offspring']), 'Offspring', 'DNA Page 3')
    
    if success_count != 3:
        print("Failed to load all profiles. Please check your files and try again.")
        return
    
    print()
    
    # Run the analysis
    print("Running parentage analysis...")
    results = analyzer.analyze_parentage('Mother', 'Father', 'Offspring')
    
    if results is None:
        print("Analysis failed.")
        return
    
    print()
    
    # Export detailed report
    print("Exporting detailed report...")
    analyzer.export_detailed_report(str(files['results']))
    
    print()
    print("Analysis complete!")
    print(f"Summary: {results['consistent_markers']}/{results['testable_markers']} markers consistent")
    print(f"Confidence: {results['confidence_level']}")
    print(f"Full report: {files['results']}")


if __name__ == "__main__":
    main()