# Testing Guide

## 🧪 Complete Testing Scenarios

### 1. Basic Complaint Submission

#### Test Case 1.1: High Priority Road Damage
**Input:**
- Name: Rajesh Kumar
- Email: rajesh@example.com
- Phone: +91 9876543210
- Category: Road Damage
- Description: "URGENT! Major pothole on Station Road near Railway Crossing. Multiple accidents reported. Two-wheeler fell yesterday causing serious injury. Immediate repair needed to prevent more accidents."
- Location: Click on map or use current location
- Image: Upload photo of pothole

**Expected Result:**
- Priority: Critical or High (score 70+)
- Status: Pending
- Department: Public Works Department
- Success message with complaint ID
- No duplicate warning (first complaint)

#### Test Case 1.2: Medium Priority Streetlight
**Input:**
- Name: Priya Sharma
- Email: priya@example.com
- Phone: +91 9876543211
- Category: Streetlight
- Description: "Street light not working on Park Avenue for past 3 days. Need repair."
- Location: Different area from Test 1.1
- Image: None

**Expected Result:**
- Priority: Medium (score 30-49)
- Status: Pending
- Department: Electricity Department

#### Test Case 1.3: Auto-Categorization
**Input:**
- Name: Amit Verma
- Email: amit@example.com
- Category: Auto-Detect from Description
- Description: "Garbage bins overflowing on MG Road. Waste not collected for 5 days. Bad smell and flies everywhere."
- Location: Select on map
- Image: Upload garbage photo

**Expected Result:**
- Auto-detected Category: Waste Management
- Priority: High (due to keywords and image)
- Department: Sanitation Department

### 2. Duplicate Detection

#### Test Case 2.1: Submit Similar Complaint
**Input:**
- Description: "Large pothole on Station Road causing accidents. Needs urgent repair."
- Same category and nearby location as Test 1.1

**Expected Result:**
- is_duplicate: true
- similar_count: 1
- Warning message showing similar complaint found
- Still created but linked to original

### 3. Admin Dashboard

#### Test Case 3.1: View Statistics
**Steps:**
1. Navigate to http://localhost:5000/admin
2. Check statistics cards

**Expected Result:**
- Total complaints: 3 (from above tests)
- Pending: 3
- In Progress: 0
- Resolved: 0
- Charts showing category and priority distribution

#### Test Case 3.2: Filter Complaints
**Steps:**
1. On admin dashboard
2. Select Priority Filter: "High"
3. Select Status Filter: "Pending"

**Expected Result:**
- Only high priority pending complaints shown
- Other rows hidden

#### Test Case 3.3: Update Complaint Status
**Steps:**
1. Click eye icon on first complaint
2. View detailed information
3. Close details
4. Click edit icon
5. Change status to "In Progress"
6. Add note: "Assigned to field team"
7. Click Update

**Expected Result:**
- Status updated successfully
- Badge changes to "In Progress"
- Statistics updated
- Timestamp updated

### 4. Map Functionality

#### Test Case 4.1: View All Complaints on Map
**Steps:**
1. Navigate to http://localhost:5000/map
2. Observe markers

**Expected Result:**
- 3 markers visible (or clusters if same location)
- Critical/High priority: Red/Orange markers
- Medium priority: Blue markers
- Legend shows correct counts

#### Test Case 4.2: Click Marker for Details
**Steps:**
1. Click on a marker
2. Read popup

**Expected Result:**
- Popup shows:
  - Complaint ID and category
  - Priority badge (colored)
  - Status
  - Department
  - Description (truncated)
  - Image (if uploaded)
  - Address
  - Date

### 5. ML Priority Testing

#### Test Case 5.1: Critical Priority Keywords
**Input Description:**
"EMERGENCY! Building wall collapsed on Main Street. Danger to public safety. Risk of serious injury or death. Immediate action required!"

**Expected Priority:** Critical (80-90 score)

**Reason:**
- Critical keywords: emergency, collapsed, danger, death, immediate
- Critical category: Building Safety
- Detailed description
- Multiple urgency indicators

#### Test Case 5.2: Low Priority Test
**Input Description:**
"Park bench needs painting"

**Expected Priority:** Low (20-30 score)

**Reason:**
- No critical/high keywords
- Low-impact category
- Short description
- No urgency
- No image

#### Test Case 5.3: Priority Boost from Frequency
**Steps:**
1. Submit 3 complaints about potholes in same area
2. Submit 4th complaint about pothole in same area

**Expected Result:**
- 4th complaint gets higher priority score
- Frequency boost applied (up to 15 points)

### 6. Image Upload

#### Test Case 6.1: Valid Image Upload
**Input:**
- Upload JPG, PNG, or WEBP image
- Size < 5MB

**Expected Result:**
- Image uploaded successfully
- Preview shown
- Priority boost of 10 points
- Image displayed in admin view

#### Test Case 6.2: Invalid File Type
**Input:**
- Try to upload .pdf or .exe file

**Expected Result:**
- File rejected
- Error message
- Form not submitted

#### Test Case 6.3: Large File
**Input:**
- Upload image > 5MB

**Expected Result:**
- File rejected
- Size error message

### 7. Location Features

#### Test Case 7.1: Current Location
**Steps:**
1. Click "Use My Current Location" button
2. Allow browser location access

**Expected Result:**
- Map zooms to current location
- Marker placed at current position
- Latitude/longitude filled
- Address auto-filled (reverse geocoding)

#### Test Case 7.2: Manual Location Selection
**Steps:**
1. Click anywhere on map
2. Observe marker placement

**Expected Result:**
- Marker placed at clicked location
- Coordinates updated
- Address fetched

### 8. Edge Cases

#### Test Case 8.1: Submit Without Location
**Steps:**
1. Fill form
2. Don't select location
3. Click Submit

**Expected Result:**
- Validation error
- Alert: "Please select a location on the map"
- Form not submitted

#### Test Case 8.2: Empty Description
**Steps:**
1. Fill form but leave description empty
2. Try to submit

**Expected Result:**
- HTML5 validation error
- Required field highlighted
- Form not submitted

#### Test Case 8.3: Invalid Email
**Input:** email@invalid

**Expected Result:**
- Email validation error
- Form not submitted

### 9. Responsive Design

#### Test Case 9.1: Mobile View
**Steps:**
1. Open DevTools
2. Toggle device toolbar
3. Select mobile device (e.g., iPhone 12)
4. Navigate through all pages

**Expected Result:**
- Layout adjusts to mobile
- Navigation becomes hamburger (if implemented)
- Forms stack vertically
- Buttons touch-friendly
- Map remains functional

#### Test Case 9.2: Tablet View
**Device:** iPad (768px width)

**Expected Result:**
- Two-column layouts maintained where appropriate
- Charts responsive
- Table scrollable if needed

### 10. Performance Testing

#### Test Case 10.1: Multiple Submissions
**Steps:**
1. Submit 50 complaints with varying data
2. Check admin dashboard load time
3. Check map view performance

**Expected Result:**
- Dashboard loads in < 3 seconds
- Map uses clustering for 50+ markers
- Filters work smoothly
- No browser lag

#### Test Case 10.2: Large Description
**Input:**
- 500+ word description

**Expected Result:**
- Accepted without issues
- Displayed correctly (may truncate in lists)
- Full text in detail view

### 11. API Testing

#### Test Case 11.1: Get All Complaints
```bash
curl http://localhost:5000/api/complaints
```

**Expected Result:**
```json
{
    "success": true,
    "complaints": [...]
}
```

#### Test Case 11.2: Get Single Complaint
```bash
curl http://localhost:5000/api/complaints/1
```

**Expected Result:**
```json
{
    "success": true,
    "complaint": {...}
}
```

#### Test Case 11.3: Update Complaint
```bash
curl -X POST http://localhost:5000/api/complaints/1/update \
  -H "Content-Type: application/json" \
  -d '{"status": "Resolved", "notes": "Fixed on 2026-01-26"}'
```

**Expected Result:**
```json
{
    "success": true,
    "message": "Complaint updated successfully",
    "complaint": {...}
}
```

### 12. Security Testing

#### Test Case 12.1: SQL Injection Attempt
**Input Description:**
```
'; DROP TABLE complaints; --
```

**Expected Result:**
- Input stored as plain text
- No SQL executed
- Supabase prevents injection

#### Test Case 12.2: XSS Attempt
**Input Description:**
```html
<script>alert('XSS')</script>
```

**Expected Result:**
- Script not executed
- Displayed as plain text or sanitized

#### Test Case 12.3: Large File Upload
**Input:**
- 100MB file

**Expected Result:**
- Rejected before upload
- Size limit enforced

## 🔍 Automated Testing (Future Implementation)

### Unit Tests Example

```python
# test_ml_models.py
import unittest
from ml_models import ComplaintPrioritizer

class TestPrioritizer(unittest.TestCase):
    def setUp(self):
        self.prioritizer = ComplaintPrioritizer()
    
    def test_critical_priority(self):
        desc = "EMERGENCY! Danger to public. Immediate action needed."
        priority, score = self.prioritizer.calculate_priority_score(
            desc, "Building Safety", 1
        )
        self.assertGreaterEqual(score, 70)
        self.assertEqual(priority, "Critical")
    
    def test_low_priority(self):
        desc = "Park bench needs paint"
        priority, score = self.prioritizer.calculate_priority_score(
            desc, "Parks & Gardens", 0
        )
        self.assertLess(score, 30)
        self.assertEqual(priority, "Low")
    
    def test_categorization(self):
        desc = "Large pothole on main road"
        category = self.prioritizer.categorize_complaint(desc)
        self.assertEqual(category, "Road Damage")

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m unittest test_ml_models.py
```

## 📊 Test Report Template

After testing, document results:

```
TEST EXECUTION REPORT
Date: YYYY-MM-DD
Tester: [Name]

SUMMARY:
- Total Test Cases: 30
- Passed: 28
- Failed: 2
- Blocked: 0
- Pass Rate: 93.3%

FAILED TEST CASES:
1. Test Case 8.2
   - Issue: Empty description not validated on old browsers
   - Severity: Low
   - Fix: Add JavaScript validation

2. Test Case 10.1
   - Issue: Map slow with 100+ markers without clustering
   - Severity: Medium
   - Fix: Ensure clustering enabled

RECOMMENDATIONS:
- Add loading indicators
- Implement pagination for large datasets
- Add comprehensive error handling
```

## 🚀 Next Steps After Testing

1. **Fix all critical bugs**
2. **Optimize performance issues**
3. **Add user authentication**
4. **Implement email notifications**
5. **Deploy to production**
6. **Monitor and iterate**
