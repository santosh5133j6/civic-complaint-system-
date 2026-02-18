# Supabase Database Schema

This document outlines the database schema for the Civic Issue Reporting System.

## Setup Instructions

1. Create a new Supabase project at https://supabase.com
2. Go to the SQL Editor in your Supabase dashboard
3. Run the following SQL commands to create the necessary tables

## SQL Schema

```sql
-- Create users table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create complaints table
CREATE TABLE complaints (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    priority VARCHAR(50) NOT NULL,
    priority_score INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'Pending',
    department VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    address TEXT,
    image_url TEXT,
    is_duplicate BOOLEAN DEFAULT FALSE,
    similar_count INTEGER DEFAULT 0,
    admin_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_complaints_status ON complaints(status);
CREATE INDEX idx_complaints_priority ON complaints(priority);
CREATE INDEX idx_complaints_category ON complaints(category);
CREATE INDEX idx_complaints_created_at ON complaints(created_at DESC);
CREATE INDEX idx_complaints_location ON complaints(latitude, longitude);

-- Enable Row Level Security (RLS)
ALTER TABLE complaints ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policies for public read access
CREATE POLICY "Enable read access for all users" ON complaints
    FOR SELECT USING (true);

CREATE POLICY "Enable insert access for all users" ON complaints
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update access for all users" ON complaints
    FOR UPDATE USING (true);

-- Create a function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_complaints_updated_at BEFORE UPDATE ON complaints
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## Configuration

After creating the tables, you need to configure your application:

1. Copy `.env.example` to `.env`
2. Get your Supabase credentials:
   - Go to Settings > API in your Supabase dashboard
   - Copy the Project URL and paste it as `SUPABASE_URL`
   - Copy the `anon` public key and paste it as `SUPABASE_KEY`

3. Update the `.env` file:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
FLASK_SECRET_KEY=your-random-secret-key
FLASK_ENV=development
```

## Storage Setup (Optional - for image uploads)

If you want to store images in Supabase Storage instead of local filesystem:

1. Go to Storage in Supabase dashboard
2. Create a new bucket named `complaint-images`
3. Set the bucket to public
4. Update the file upload logic in `app.py` to use Supabase Storage

```python
# Example code for Supabase Storage upload
def upload_to_supabase(file):
    supabase = get_supabase()
    file_name = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}"
    
    supabase.storage.from_('complaint-images').upload(
        file_name,
        file.read()
    )
    
    return supabase.storage.from_('complaint-images').get_public_url(file_name)
```

## Sample Data (Optional)

To test the application, you can insert some sample data:

```sql
INSERT INTO complaints (name, email, phone, description, category, priority, priority_score, status, department, latitude, longitude, address)
VALUES 
    ('John Doe', 'john@example.com', '+91 9876543210', 'Large pothole on Main Street causing traffic issues and accidents. Urgent repair needed.', 'Road Damage', 'Critical', 85, 'Pending', 'Public Works Department', 23.3441, 85.3096, 'Main Street, Ranchi'),
    ('Jane Smith', 'jane@example.com', '+91 9876543211', 'Garbage not collected for 5 days. Accumulation causing health hazard.', 'Waste Management', 'High', 65, 'In Progress', 'Sanitation Department', 23.3542, 85.3347, 'Gandhi Nagar, Ranchi'),
    ('Bob Johnson', 'bob@example.com', '+91 9876543212', 'Street light not working for 2 weeks', 'Streetlight', 'Medium', 45, 'Pending', 'Electricity Department', 23.3689, 85.3340, 'Park Road, Ranchi');
```

## Table Descriptions

### complaints
- Stores all citizen-submitted complaints
- Includes location data (latitude/longitude)
- Tracks status, priority, and department assignment
- Stores ML-generated priority scores
- Includes duplicate detection flags

### users (Optional)
- Stores user information
- Can be used for authentication and user management
- Currently not fully implemented in the basic version

## API Access

The Supabase JavaScript client automatically handles API calls. The Python library uses the same REST API endpoints.

### Direct API Examples:

```bash
# Get all complaints
curl 'https://your-project.supabase.co/rest/v1/complaints' \
  -H "apikey: your-anon-key" \
  -H "Authorization: Bearer your-anon-key"

# Create a complaint
curl -X POST 'https://your-project.supabase.co/rest/v1/complaints' \
  -H "apikey: your-anon-key" \
  -H "Authorization: Bearer your-anon-key" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", ...}'
```
