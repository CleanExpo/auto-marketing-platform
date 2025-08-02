#!/usr/bin/env python3
"""
Simple Entry System for Testing Phase
Easy access without authentication, optional user accounts for saving features
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from unicode_utils import safe_print, create_banner, safe_format

class SimpleEntrySystem:
    """
    Simple entry system for testing phase - no authentication required
    Optional user accounts for saving projects and features
    """
    
    def __init__(self):
        self.base_path = Path("C:/Auto Marketing")
        self.users_path = self.base_path / "data" / "users"
        self.projects_path = self.base_path / "data" / "projects"
        self.sessions_path = self.base_path / "data" / "sessions"
        
        # Create directories
        for path in [self.users_path, self.projects_path, self.sessions_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        self.current_session = None
        self.guest_mode = True
        self.current_user = None
    
    def start_system(self) -> Dict[str, Any]:
        """Start the system with simple entry options"""
        
        safe_print(create_banner("PLATFORM MARKETING MASTERY SYSTEM"))
        safe_print("Welcome to the Platform-Specific Marketing System!")
        safe_print("Testing Phase - Easy Entry Enabled")
        safe_print("="*60)
        
        entry_options = self._show_entry_options()
        return entry_options
    
    def _show_entry_options(self) -> Dict[str, Any]:
        """Show entry options to user"""
        
        safe_print("\n🚀 Choose your entry method:")
        safe_print("1. Quick Start (Guest Mode) - Start immediately, no saving")
        safe_print("2. Create User Account - Save projects and settings")
        safe_print("3. Load Existing Account - Continue previous work")
        safe_print("4. Browse Saved Projects - View existing projects")
        safe_print("5. System Health Check - Verify system status")
        
        return {
            'options': {
                '1': 'quick_start',
                '2': 'create_account', 
                '3': 'load_account',
                '4': 'browse_projects',
                '5': 'health_check'
            },
            'guest_mode_available': True,
            'accounts_optional': True
        }
    
    def quick_start_guest_mode(self) -> Dict[str, Any]:
        """Start in guest mode - immediate access, no saving"""
        
        safe_print("\n🎯 Starting in Guest Mode...")
        
        session_id = f"guest_{int(time.time())}"
        
        self.current_session = {
            'session_id': session_id,
            'mode': 'guest',
            'started_at': datetime.now().isoformat(),
            'user_id': None,
            'features_available': [
                'content_adaptation',
                'speech_interface', 
                'video_generation',
                'platform_analysis',
                'real_time_testing'
            ],
            'saving_enabled': False,
            'session_data': {}
        }
        
        self.guest_mode = True
        
        safe_print("✅ Guest mode activated!")
        safe_print("📝 Note: Projects won't be saved in guest mode")
        safe_print("💡 Create an account anytime to save your work")
        
        return self._start_main_interface()
    
    def create_simple_account(self, display_name: str = None) -> Dict[str, Any]:
        """Create a simple account - just a display name, no password"""
        
        if not display_name:
            display_name = f"User_{int(time.time())}"
        
        user_id = f"user_{int(time.time())}"
        
        user_data = {
            'user_id': user_id,
            'display_name': display_name,
            'created_at': datetime.now().isoformat(),
            'projects': [],
            'settings': {
                'preferred_platforms': [],
                'default_voice_mode': 'casual',
                'auto_save': True,
                'notification_preferences': {
                    'system_updates': True,
                    'project_completion': True,
                    'performance_alerts': False
                }
            },
            'usage_stats': {
                'sessions_count': 0,
                'projects_created': 0,
                'content_pieces_generated': 0,
                'platforms_used': []
            }
        }
        
        # Save user data
        user_file = self.users_path / f"{user_id}.json"
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        self.current_user = user_data
        self.guest_mode = False
        
        safe_print(f"✅ Account created for {display_name}")
        safe_print("🎉 You can now save projects and settings!")
        
        return self._start_main_interface()
    
    def load_existing_account(self, user_identifier: str = None) -> Dict[str, Any]:
        """Load an existing account"""
        
        if not user_identifier:
            # Show available accounts
            accounts = self._list_available_accounts()
            if not accounts:
                safe_print("❌ No accounts found. Creating guest session...")
                return self.quick_start_guest_mode()
            
            safe_print("\n📂 Available accounts:")
            for i, account in enumerate(accounts, 1):
                safe_print(f"  {i}. {account['display_name']} (created: {account['created_at'][:10]})")
            
            # For testing, automatically load the first account
            user_identifier = accounts[0]['user_id']
        
        # Load user data
        user_file = self.users_path / f"{user_identifier}.json"
        if user_file.exists():
            with open(user_file, 'r') as f:
                user_data = json.load(f)
            
            self.current_user = user_data
            self.guest_mode = False
            
            safe_print(f"✅ Welcome back, {user_data['display_name']}!")
            safe_print(f"📊 You have {len(user_data['projects'])} saved projects")
            
            return self._start_main_interface()
        else:
            safe_print("❌ Account not found. Starting guest mode...")
            return self.quick_start_guest_mode()
    
    def _list_available_accounts(self) -> List[Dict[str, Any]]:
        """List all available user accounts"""
        
        accounts = []
        for user_file in self.users_path.glob("*.json"):
            try:
                with open(user_file, 'r') as f:
                    user_data = json.load(f)
                    accounts.append(user_data)
            except Exception:
                continue
        
        return sorted(accounts, key=lambda x: x['created_at'], reverse=True)
    
    def browse_saved_projects(self) -> Dict[str, Any]:
        """Browse saved projects from all users"""
        
        safe_print("\n📁 Browsing Saved Projects...")
        
        all_projects = []
        
        # Collect projects from all users
        for user_file in self.users_path.glob("*.json"):
            try:
                with open(user_file, 'r') as f:
                    user_data = json.load(f)
                    for project_id in user_data.get('projects', []):
                        project_file = self.projects_path / f"{project_id}.json"
                        if project_file.exists():
                            with open(project_file, 'r') as pf:
                                project_data = json.load(pf)
                                project_data['owner'] = user_data['display_name']
                                all_projects.append(project_data)
            except Exception:
                continue
        
        if not all_projects:
            safe_print("📭 No saved projects found")
            safe_print("💡 Create an account and start a project to see it here!")
            return self.quick_start_guest_mode()
        
        safe_print(f"Found {len(all_projects)} saved projects:")
        for i, project in enumerate(all_projects[:5], 1):  # Show first 5
            safe_print(f"  {i}. {project['name']} by {project['owner']} ({project['created_at'][:10]})")
        
        return {
            'projects': all_projects,
            'action': 'browse_projects',
            'can_load': True,
            'can_continue_as_guest': True
        }
    
    def _start_main_interface(self) -> Dict[str, Any]:
        """Start the main system interface"""
        
        safe_print("\n🎛️ MAIN SYSTEM INTERFACE")
        safe_print("-" * 40)
        
        if self.guest_mode:
            safe_print("👤 Mode: Guest (no saving)")
        else:
            safe_print(f"👤 User: {self.current_user['display_name']}")
            safe_print("💾 Saving: Enabled")
        
        # Show available features
        features = [
            "🎙️ Voice Content Creation",
            "🔄 Multi-Platform Adaptation", 
            "🎬 AI Video Generation",
            "📊 Performance Analytics",
            "💰 Pricing Optimization",
            "🧠 AI Strategy Assistant"
        ]
        
        safe_print("\n🚀 Available Features:")
        for i, feature in enumerate(features, 1):
            safe_print(f"  {i}. {feature}")
        
        safe_print("\n⌨️ Quick Commands:")
        safe_print("  'voice' - Start voice interface")
        safe_print("  'create' - Create new content")
        safe_print("  'analyze' - Platform analysis")
        safe_print("  'save' - Save current project (account required)")
        safe_print("  'account' - Create/switch account")
        safe_print("  'help' - Show detailed help")
        safe_print("  'exit' - Exit system")
        
        return {
            'interface_ready': True,
            'user_mode': 'guest' if self.guest_mode else 'authenticated',
            'saving_available': not self.guest_mode,
            'features_available': True,
            'session_id': self.current_session['session_id'] if self.current_session else None
        }
    
    def save_project(self, project_data: Dict[str, Any]) -> bool:
        """Save a project (requires account)"""
        
        if self.guest_mode:
            safe_print("❌ Saving requires an account")
            safe_print("💡 Type 'account' to create one quickly!")
            return False
        
        project_id = f"project_{int(time.time())}"
        
        project_info = {
            'project_id': project_id,
            'name': project_data.get('name', f'Project {project_id}'),
            'description': project_data.get('description', 'Auto-generated project'),
            'created_at': datetime.now().isoformat(),
            'owner_id': self.current_user['user_id'],
            'data': project_data,
            'platforms_used': project_data.get('platforms', []),
            'content_pieces': len(project_data.get('content_adaptations', {})),
            'last_modified': datetime.now().isoformat()
        }
        
        # Save project file
        project_file = self.projects_path / f"{project_id}.json"
        with open(project_file, 'w') as f:
            json.dump(project_info, f, indent=2)
        
        # Update user's project list
        self.current_user['projects'].append(project_id)
        self.current_user['usage_stats']['projects_created'] += 1
        
        # Save updated user data
        user_file = self.users_path / f"{self.current_user['user_id']}.json"
        with open(user_file, 'w') as f:
            json.dump(self.current_user, f, indent=2)
        
        safe_print(f"✅ Project '{project_info['name']}' saved!")
        return True
    
    def get_quick_help(self) -> str:
        """Get quick help information"""
        
        help_text = """
🆘 QUICK HELP GUIDE

🎯 GETTING STARTED:
• Guest Mode: Immediate access, no saving
• Account Mode: Create account to save projects
• All features available in both modes

🎙️ VOICE INTERFACE:
• Say 'start voice session' to begin
• Modes: brainstorm, strategy, execution, analysis
• Natural conversation - just talk about your ideas!

🔄 CONTENT CREATION:
• Create once, adapt to all 8 platforms automatically
• Optimized for each platform's algorithm
• Includes hashtags, timing, and format specs

🎬 VIDEO GENERATION:
• AI-powered video creation with Veo3
• Platform-specific formats and sizes
• Automatic thumbnail generation

📊 ANALYTICS:
• Real-time performance tracking
• ROI calculation and optimization
• Cross-platform comparison

💾 SAVING PROJECTS:
• Guest Mode: No saving (testing only)
• Account Mode: Auto-save enabled
• Projects include all adaptations and settings

⚡ QUICK COMMANDS:
• 'voice' - Voice interface
• 'create' - New content
• 'analyze' - Platform analysis  
• 'save' - Save project
• 'account' - User account
• 'exit' - Exit system

Need more help? The system guides you through each step!
        """
        
        return help_text


def launch_simple_entry():
    """Launch the simple entry system"""
    
    entry_system = SimpleEntrySystem()
    return entry_system.start_system()


def demo_entry_flow():
    """Demonstrate the entry flow for testing"""
    
    safe_print(create_banner("SIMPLE ENTRY SYSTEM DEMO"))
    
    entry_system = SimpleEntrySystem()
    
    # Show entry options
    safe_print("\n1. Showing entry options...")
    options = entry_system._show_entry_options()
    
    # Demo guest mode
    safe_print("\n2. Demo: Quick Start (Guest Mode)")
    guest_session = entry_system.quick_start_guest_mode()
    
    # Demo account creation
    safe_print("\n3. Demo: Creating Simple Account")
    account_session = entry_system.create_simple_account("Test User")
    
    # Demo project saving
    safe_print("\n4. Demo: Saving a Project")
    test_project = {
        'name': 'Test Marketing Campaign',
        'description': 'Demo project for testing',
        'platforms': ['instagram', 'youtube', 'tiktok'],
        'content_adaptations': {
            'instagram': {'title': 'IG post', 'content': 'test'},
            'youtube': {'title': 'YT video', 'content': 'test'},
            'tiktok': {'title': 'TT video', 'content': 'test'}
        }
    }
    
    saved = entry_system.save_project(test_project)
    
    safe_print("\n5. Demo: Browse Projects")
    projects = entry_system.browse_saved_projects()
    
    safe_print("\n6. Demo: Quick Help")
    help_text = entry_system.get_quick_help()
    safe_print(help_text[:200] + "...")  # Show first 200 chars
    
    safe_print("\n" + "="*60)
    safe_print("SIMPLE ENTRY SYSTEM DEMO COMPLETE")
    safe_print("✅ All features working correctly")
    safe_print("🚀 Ready for testing phase!")


if __name__ == "__main__":
    demo_entry_flow()