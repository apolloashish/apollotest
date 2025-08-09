"""
Configuration module for Moodle Connectivity
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for Moodle connectivity settings"""
    
    # Moodle Server Configuration
    MOODLE_BASE_URL = os.getenv('MOODLE_BASE_URL')
    MOODLE_TOKEN = os.getenv('MOODLE_TOKEN')
    MOODLE_USERNAME = os.getenv('MOODLE_USERNAME')
    MOODLE_PASSWORD = os.getenv('MOODLE_PASSWORD')
    
    # Request Configuration
    TIMEOUT = int(os.getenv('MOODLE_TIMEOUT', 15))
    MAX_RETRIES = int(os.getenv('MOODLE_MAX_RETRIES', 3))
    REQUEST_DELAY = float(os.getenv('MOODLE_REQUEST_DELAY', 0.5))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Database Configuration (if needed for caching/storage)
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Moodle Web Service Format
    WS_FORMAT = os.getenv('MOODLE_WS_FORMAT', 'json')
    
    @classmethod
    def get_moodle_client_params(cls) -> Dict[str, Any]:
        """Get parameters for Moodle client initialization"""
        return {
            'base_url': cls.MOODLE_BASE_URL,
            'token': cls.MOODLE_TOKEN,
            'timeout_seconds': cls.TIMEOUT,
        }
    
    @classmethod
    def get_request_params(cls) -> Dict[str, Any]:
        """Get default request parameters for Moodle API calls"""
        return {
            'timeout': cls.TIMEOUT,
            'max_retries': cls.MAX_RETRIES,
            'request_delay': cls.REQUEST_DELAY,
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required Moodle configuration is present"""
        required_vars = ['MOODLE_BASE_URL', 'MOODLE_TOKEN']
        missing_vars = []
        
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing required Moodle configuration: {', '.join(missing_vars)}")
            print("Please set these environment variables in your .env file:")
            for var in missing_vars:
                print(f"  - {var}")
            return False
        
        print("✅ Moodle configuration validated successfully")
        return True


# Pre-configured settings for Moodle web services
class MoodleServices:
    """Pre-configured settings for common Moodle web service functions"""
    
    # Core web services
    CORE_SERVICES = {
        'site_info': 'core_webservice_get_site_info',
        'user_by_field': 'core_user_get_users_by_field',
        'create_users': 'core_user_create_users',
        'update_users': 'core_user_update_users',
        'delete_users': 'core_user_delete_users',
    }
    
    # Course management services
    COURSE_SERVICES = {
        'get_courses': 'core_course_get_courses',
        'create_courses': 'core_course_create_courses',
        'update_courses': 'core_course_update_courses',
        'delete_courses': 'core_course_delete_courses',
        'get_course_contents': 'core_course_get_contents',
        'enrol_users': 'enrol_manual_enrol_users',
        'unenrol_users': 'enrol_manual_unenrol_users',
    }
    
    # Grade management services
    GRADE_SERVICES = {
        'get_grades': 'core_grades_get_grades',
        'update_grades': 'core_grades_update_grades',
        'get_grade_items': 'core_grading_get_definitions',
    }
    
    # Assignment services
    ASSIGNMENT_SERVICES = {
        'get_assignments': 'mod_assign_get_assignments',
        'get_submissions': 'mod_assign_get_submissions',
        'save_submission': 'mod_assign_save_submission',
        'submit_for_grading': 'mod_assign_submit_for_grading',
    }
    
    @classmethod
    def get_service_function(cls, category: str, service: str) -> str:
        """Get the Moodle function name for a specific service"""
        category_services = getattr(cls, f"{category.upper()}_SERVICES", {})
        return category_services.get(service, "")
    
    @classmethod
    def get_all_services(cls) -> Dict[str, Dict[str, str]]:
        """Get all available service categories and their functions"""
        return {
            'core': cls.CORE_SERVICES,
            'course': cls.COURSE_SERVICES,
            'grade': cls.GRADE_SERVICES,
            'assignment': cls.ASSIGNMENT_SERVICES,
        }


# Export commonly used configurations
config = Config()
moodle_services = MoodleServices()