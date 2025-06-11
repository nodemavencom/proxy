"""
Comprehensive tests for proxy building compliance with how-api-works.md
This test validates that our implementation matches the specification exactly.
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nodemaven.utils import build_proxy_username, build_proxy_url, get_proxy_config, generate_session_id


class TestProxyComplianceWithDocs:
    """Test that proxy building matches how-api-works.md specification exactly."""
    
    def test_base_proxy_format(self):
        """Test base proxy format compliance: {host}:{port}:{username}:{password}"""
        # Mock credentials for testing
        import nodemaven.utils
        original_func = nodemaven.utils.get_correct_proxy_credentials
        nodemaven.utils.get_correct_proxy_credentials = lambda: ("testuser", "testpass")
        
        try:
            # Test HTTP format
            http_url = build_proxy_url(protocol="http", country="us")
            assert "gate.nodemaven.com:8080" in http_url
            assert "testuser" in http_url
            assert "testpass" in http_url
            assert http_url.startswith("http://")
            
            # Test SOCKS5 format
            socks_url = build_proxy_url(protocol="socks5", country="us")
            assert "gate.nodemaven.com:1080" in socks_url
            assert socks_url.startswith("socks5://")
            
        finally:
            # Restore original function
            nodemaven.utils.get_correct_proxy_credentials = original_func
    
    def test_connection_types(self):
        """Test connection types: residential (default) and mobile"""
        base_username = "testuser"
        
        # Residential (default - no type specified)
        residential = build_proxy_username(base_username, country="us")
        assert "type-mobile" not in residential
        
        # Mobile (explicit)
        mobile = build_proxy_username(base_username, country="us", type="mobile")
        assert "type-mobile" in mobile
    
    def test_ip_version_support(self):
        """Test IP version support: IPv4+IPv6 (default) and IPv4 only"""
        base_username = "testuser"
        
        # Default should include ipv4-true (our implementation always adds this)
        default = build_proxy_username(base_username, country="us")
        assert "ipv4-true" in default
        
        # Explicit IPv4
        ipv4_only = build_proxy_username(base_username, country="us", ipv4=True)
        assert "ipv4-true" in ipv4_only
        
        # IPv4 false (should show false)
        ipv4_false = build_proxy_username(base_username, country="us", ipv4=False)
        assert "ipv4-false" in ipv4_false
    
    def test_location_settings_hierarchy(self):
        """Test location hierarchy: Country → Region → City → ISP"""
        base_username = "testuser"
        
        # Country only
        country_only = build_proxy_username(base_username, country="us")
        assert "country-us" in country_only
        
        # Country + Region
        with_region = build_proxy_username(base_username, country="us", region="new_york")
        assert "country-us" in with_region
        assert "region-newyork" in with_region  # spaces removed
        
        # Country + Region + City
        with_city = build_proxy_username(base_username, country="us", region="new_york", city="brooklyn")
        assert "country-us" in with_city
        assert "region-newyork" in with_city
        assert "city-brooklyn" in with_city
        
        # Full hierarchy with ISP
        full_hierarchy = build_proxy_username(
            base_username, 
            country="ru", 
            region="moscow", 
            city="moscow", 
            isp="beeline_home"
        )
        assert "country-ru" in full_hierarchy
        assert "region-moscow" in full_hierarchy
        assert "city-moscow" in full_hierarchy
        assert "isp-beelinehome" in full_hierarchy  # underscores removed
    
    def test_session_types(self):
        """Test session types: rotating (default) and sticky"""
        base_username = "testuser"
        
        # Rotating (default - no sid)
        rotating = build_proxy_username(base_username, country="us")
        assert "sid-" not in rotating
        
        # Sticky with specific session
        sticky = build_proxy_username(base_username, country="us", session="a49c071423294")
        assert "sid-a49c071423294" in sticky
        
        # Sticky with auto-generated session
        sticky_auto = build_proxy_username(base_username, country="us", sticky=True)
        assert "sid-" in sticky_auto
        # Verify session ID format (13 characters, alphanumeric)
        parts = sticky_auto.split("-")
        sid_index = parts.index("sid") + 1
        session_id = parts[sid_index]
        assert len(session_id) == 13
        assert session_id.isalnum()
    
    @pytest.mark.skip(reason="TTL functionality not yet implemented - HIGH PRIORITY")
    def test_ttl_support(self):
        """Test TTL (Time-To-Live) support for sticky sessions"""
        base_username = "testuser"
        
        # TTL test cases from documentation
        ttl_cases = [
            {"ttl": "60s", "expected": "ttl-60s"},
            {"ttl": "1m", "expected": "ttl-1m"},
            {"ttl": "5m", "expected": "ttl-5m"},
            {"ttl": "24h", "expected": "ttl-24h"}
        ]
        
        for case in ttl_cases:
            username = build_proxy_username(
                base_username, 
                country="us", 
                session="a49c071423294",
                ttl=case["ttl"]
            )
            assert case["expected"] in username
            assert "sid-a49c071423294" in username
    
    def test_ip_quality_filter(self):
        """Test IP quality filter options"""
        base_username = "testuser"
        
        # Default filter (our implementation defaults to medium)
        default = build_proxy_username(base_username, country="us")
        assert "filter-medium" in default
        
        # Explicit medium filter
        medium = build_proxy_username(base_username, country="us", filter="medium")
        assert "filter-medium" in medium
    
    def test_protocol_and_ports(self):
        """Test protocol and port combinations"""
        import nodemaven.utils
        original_func = nodemaven.utils.get_correct_proxy_credentials
        nodemaven.utils.get_correct_proxy_credentials = lambda: ("testuser", "testpass")
        
        try:
            # HTTP should use port 8080
            http_url = build_proxy_url(protocol="http", country="us")
            assert ":8080" in http_url
            
            # SOCKS5 should use port 1080
            socks_url = build_proxy_url(protocol="socks5", country="us")
            assert ":1080" in socks_url
            
        finally:
            nodemaven.utils.get_correct_proxy_credentials = original_func
    
    def test_documentation_examples_compliance(self, proxy_examples_from_docs):
        """Test exact examples from how-api-works.md documentation"""
        
        for example in proxy_examples_from_docs:
            # Skip TTL examples until TTL is implemented
            if "ttl" in example["params"]:
                pytest.skip("TTL functionality not implemented yet")
            
            # Build username with same parameters
            username = build_proxy_username("aa101d91571b74", **example["params"])
            
            # For now, test without TTL parts
            expected_without_ttl = example["expected"]
            if "-ttl-" in expected_without_ttl:
                # Remove TTL part for comparison
                parts = expected_without_ttl.split("-")
                ttl_index = parts.index("ttl")
                expected_without_ttl = "-".join(parts[:ttl_index] + parts[ttl_index+2:])
            
            # Compare the built username (this will fail until we implement missing features)
            print(f"\nTesting: {example['description']}")
            print(f"Expected: {expected_without_ttl}")
            print(f"Got:      {username}")
            
            # This assertion will help us identify what's different
            # Note: This test will initially fail and show us exactly what we need to fix
            assert username == expected_without_ttl, f"Mismatch in {example['description']}"


class TestProxyBuildingEdgeCases:
    """Test edge cases and error conditions for proxy building."""
    
    def test_empty_parameters(self):
        """Test handling of empty parameters"""
        base_username = "testuser"
        
        # Empty country should still work
        with_empty = build_proxy_username(base_username, country="", region="test")
        assert "country-" in with_empty  # Should include empty country
        
        # None values should be ignored
        with_none = build_proxy_username(base_username, country="us", region=None, city=None)
        assert "region-" not in with_none
        assert "city-" not in with_none
    
    def test_special_characters_handling(self):
        """Test handling of special characters in location names"""
        base_username = "testuser"
        
        # Test spaces and underscores (should be cleaned)
        with_spaces = build_proxy_username(base_username, region="New York", city="New_York_City")
        assert "region-newyork" in with_spaces  # spaces removed
        assert "city-newyorkcity" in with_spaces  # spaces and underscores removed
        
        # Test special characters
        with_special = build_proxy_username(base_username, city="san-francisco", isp="at&t_wireless")
        assert "city-san-francisco" in with_special  # hyphens preserved
        assert "isp-at&twileless" in with_special  # special chars handled
    
    def test_session_id_generation(self):
        """Test session ID generation functionality"""
        # Test generate_session_id function
        session1 = generate_session_id()
        session2 = generate_session_id()
        
        # Should be different
        assert session1 != session2
        
        # Should be 13 characters
        assert len(session1) == 13
        assert len(session2) == 13
        
        # Should be alphanumeric
        assert session1.isalnum()
        assert session2.isalnum()
    
    def test_proxy_config_dictionary_structure(self):
        """Test proxy configuration dictionary for requests library"""
        import nodemaven.utils
        original_func = nodemaven.utils.get_correct_proxy_credentials
        nodemaven.utils.get_correct_proxy_credentials = lambda: ("testuser", "testpass")
        
        try:
            config = get_proxy_config(country="us", city="newyork")
            
            # Should have http and https keys
            assert "http" in config
            assert "https" in config
            
            # Both should point to same proxy URL
            assert config["http"] == config["https"]
            
            # Should contain expected components
            proxy_url = config["http"]
            assert "testuser" in proxy_url
            assert "country-us" in proxy_url
            assert "city-newyork" in proxy_url
            assert "gate.nodemaven.com:8080" in proxy_url
            
        finally:
            nodemaven.utils.get_correct_proxy_credentials = original_func


class TestMissingFunctionality:
    """Test cases for functionality that should exist but is currently missing."""
    
    def test_ttl_parsing_validation(self):
        """Test TTL format validation (not yet implemented)"""
        pytest.skip("TTL functionality needs to be implemented")
        
        # When implemented, should validate:
        # - "60s", "1m", "5m", "1h", "24h" formats
        # - Invalid formats should raise ValueError
        # - TTL should be included in proxy username when specified
    
    def test_comprehensive_parameter_validation(self):
        """Test comprehensive parameter validation"""
        pytest.skip("Enhanced validation needs to be implemented")
        
        # When implemented, should validate:
        # - Country codes (ISO format)
        # - Session ID format
        # - TTL duration formats
        # - Filter options
    
    def test_documentation_compliance_100_percent(self):
        """Test 100% compliance with how-api-works.md"""
        pytest.skip("Full compliance testing requires TTL implementation")
        
        # This test should pass when all missing functionality is implemented


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 