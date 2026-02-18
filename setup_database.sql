-- ========================================
-- Civic Issue Reporter - Database Setup
-- ========================================

-- 1. Create admins table
CREATE TABLE IF NOT EXISTS admins (
    id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    department TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Create complaints table
CREATE TABLE IF NOT EXISTS complaints (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    priority TEXT DEFAULT 'Medium',
    priority_score NUMERIC DEFAULT 50,
    status TEXT DEFAULT 'Pending',
    department TEXT,
    latitude NUMERIC,
    longitude NUMERIC,
    address TEXT,
    image_url TEXT,
    is_duplicate BOOLEAN DEFAULT FALSE,
    similar_count INTEGER DEFAULT 0,
    admin_username TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints(status);
CREATE INDEX IF NOT EXISTS idx_complaints_category ON complaints(category);
CREATE INDEX IF NOT EXISTS idx_complaints_priority ON complaints(priority);
CREATE INDEX IF NOT EXISTS idx_complaints_department ON complaints(department);
CREATE INDEX IF NOT EXISTS idx_complaints_created_at ON complaints(created_at);
CREATE INDEX IF NOT EXISTS idx_admins_username ON admins(username);
CREATE INDEX IF NOT EXISTS idx_admins_department ON admins(department);

-- 4. Create trigger for auto-updating updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_complaints_updated_at
    BEFORE UPDATE ON complaints
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 5. Enable Row Level Security (RLS)
ALTER TABLE admins ENABLE ROW LEVEL SECURITY;
ALTER TABLE complaints ENABLE ROW LEVEL SECURITY;

-- 6. Create RLS policies (allow all for now - restrict later)
CREATE POLICY "Allow all operations on admins" ON admins FOR ALL USING (true);
CREATE POLICY "Allow all operations on complaints" ON complaints FOR ALL USING (true);

-- 7. Insert default admin account
-- Password: 123 (hash: a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3)
INSERT INTO admins (username, email, password_hash, department)
VALUES ('admin', 'admin@civic.gov', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'General Administration')
ON CONFLICT (username) DO NOTHING;

-- ========================================
-- Success! Tables created.
-- Next step: Create Storage Bucket
-- ========================================
-- Go to Storage in Supabase Dashboard and create:
-- Bucket name: complaint-images
-- Public bucket: Yes
-- File size limit: 45 MB
-- Allowed MIME types: image/jpeg, image/png, image/jpg, image/gif, image/webp
