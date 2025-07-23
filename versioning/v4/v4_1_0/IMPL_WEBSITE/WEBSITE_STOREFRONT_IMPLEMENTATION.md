# MAO Website Storefront Implementation

## 💰 **SUBSCRIPTION EMPIRE ARCHITECTURE**

**Vision**: Transform MAO from local tool to **global SaaS powerhouse** with subscription-based config marketplace, crypto payments, and NFT-powered creator economy

**Revenue Streams**:
1. **Config Subscriptions**: $29.99/month unlimited downloads
2. **Premium Tiers**: $99.99/month for enterprise configs  
3. **Creator Revenue Share**: 70% to config creators, 30% to MAO
4. **NFT Minting**: $9.99 per config mint + 5% royalties
5. **Crypto Payments**: Accept BTC, ETH, SOL, USDC

---

## 🏗️ **TECHNICAL ARCHITECTURE**

### Frontend Stack
```
Next.js 14 + TypeScript + Tailwind CSS
├── Authentication: NextAuth.js with passkey support
├── Payments: Stripe + Coinbase Commerce
├── NFT Integration: Solana Web3.js
├── Multilingual: next-i18next
└── Analytics: Vercel Analytics + PostHog
```

### Backend Stack
```
Vercel Functions + Supabase
├── Database: PostgreSQL (Supabase)
├── File Storage: Supabase Storage
├── Real-time: Supabase Realtime
├── Auth: Supabase Auth + Custom Passkey
└── Payments: Stripe Webhooks + Crypto APIs
```

### Database Schema
```sql
-- Users and Subscriptions
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    display_name TEXT,
    language_code VARCHAR(5) DEFAULT 'en',
    subscription_tier VARCHAR(50) DEFAULT 'free',
    stripe_customer_id TEXT,
    crypto_wallet_address TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    tier VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    stripe_subscription_id TEXT,
    crypto_payment_address TEXT
);

-- Config Marketplace
CREATE TABLE config_collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    creator_id UUID REFERENCES users(id),
    title TEXT NOT NULL,
    description TEXT,
    category VARCHAR(50),
    price_usd DECIMAL(10,2),
    nft_mint_address TEXT,
    download_count INTEGER DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE config_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    collection_id UUID REFERENCES config_collections(id),
    file_name TEXT NOT NULL,
    file_type VARCHAR(50),
    file_content JSONB,
    storage_path TEXT
);

CREATE TABLE user_downloads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    collection_id UUID REFERENCES config_collections(id),
    downloaded_at TIMESTAMP DEFAULT NOW(),
    nft_token_id TEXT
);

-- Analytics and Tracking
CREATE TABLE usage_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action_type VARCHAR(50),
    metadata JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

---

## 🎨 **HOMEPAGE/STOREFRONT DESIGN**

### Hero Section
```jsx
// components/HeroSection.tsx
export default function HeroSection() {
    const { t } = useTranslation();
    
    return (
        <section className="bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
            <div className="container mx-auto px-4 py-24">
                <div className="text-center max-w-4xl mx-auto">
                    <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                        {t('hero.title')}
                    </h1>
                    <p className="text-xl text-slate-300 mb-8">
                        {t('hero.subtitle')}
                    </p>
                    
                    {/* Feature Pills */}
                    <div className="flex flex-wrap justify-center gap-3 mb-12">
                        <FeaturePill icon="🌍" text={t('features.multilingual')} />
                        <FeaturePill icon="⚡" text={t('features.instant_setup')} />
                        <FeaturePill icon="🔐" text={t('features.passkey_auth')} />
                        <FeaturePill icon="₿" text={t('features.crypto_payments')} />
                        <FeaturePill icon="🎨" text={t('features.nft_configs')} />
                    </div>
                    
                    {/* CTA Buttons */}
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                            {t('cta.start_free')}
                        </Button>
                        <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-slate-900">
                            {t('cta.view_marketplace')}
                        </Button>
                    </div>
                </div>
            </div>
        </section>
    );
}
```

### Subscription Pricing Section
```jsx
// components/PricingSection.tsx
export default function PricingSection() {
    const pricingTiers = [
        {
            name: 'Free',
            price: '$0',
            features: [
                '5 config downloads/month',
                'Basic workflow templates',
                'Community support',
                'Standard tools'
            ],
            cta: 'Get Started',
            popular: false
        },
        {
            name: 'Pro',
            price: '$29.99',
            features: [
                'Unlimited config downloads',
                'Premium workflow collections',
                'Priority support',
                'Advanced tools',
                'Multilingual support',
                'Analytics dashboard'
            ],
            cta: 'Start Pro Trial',
            popular: true
        },
        {
            name: 'Enterprise',
            price: '$99.99',
            features: [
                'Everything in Pro',
                'Custom integrations',
                'Dedicated support',
                'White-label options',
                'Advanced analytics',
                'Team collaboration'
            ],
            cta: 'Contact Sales',
            popular: false
        }
    ];
    
    return (
        <section className="py-24 bg-slate-50">
            <div className="container mx-auto px-4">
                <div className="text-center mb-16">
                    <h2 className="text-4xl font-bold mb-4">Choose Your Plan</h2>
                    <p className="text-xl text-slate-600">Scale with the plan that fits your needs</p>
                </div>
                
                <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                    {pricingTiers.map((tier) => (
                        <PricingCard key={tier.name} tier={tier} />
                    ))}
                </div>
            </div>
        </section>
    );
}
```

---

## 🛒 **MARKETPLACE IMPLEMENTATION**

### Config Store Interface
```jsx
// pages/marketplace.tsx
export default function Marketplace() {
    const [configs, setConfigs] = useState([]);
    const [filters, setFilters] = useState({
        category: 'all',
        priceRange: 'all',
        sortBy: 'popular'
    });
    
    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex flex-col lg:flex-row gap-8">
                {/* Filters Sidebar */}
                <div className="lg:w-64">
                    <MarketplaceFilters filters={filters} onFiltersChange={setFilters} />
                </div>
                
                {/* Config Grid */}
                <div className="flex-1">
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {configs.map((config) => (
                            <ConfigCard 
                                key={config.id} 
                                config={config}
                                onPurchase={handlePurchase}
                                onPreview={handlePreview}
                            />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

// components/ConfigCard.tsx
function ConfigCard({ config, onPurchase, onPreview }) {
    return (
        <Card className="group hover:shadow-xl transition-all duration-300">
            <div className="aspect-video bg-gradient-to-br from-blue-500 to-purple-600 rounded-t-lg p-6 flex items-center justify-center">
                <div className="text-center text-white">
                    <div className="text-4xl mb-2">{config.icon}</div>
                    <h3 className="font-semibold">{config.title}</h3>
                </div>
            </div>
            
            <CardContent className="p-6">
                <p className="text-slate-600 mb-4 line-clamp-3">{config.description}</p>
                
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                        <Avatar className="h-6 w-6">
                            <AvatarImage src={config.creator.avatar} />
                            <AvatarFallback>{config.creator.name[0]}</AvatarFallback>
                        </Avatar>
                        <span className="text-sm text-slate-600">{config.creator.name}</span>
                    </div>
                    <div className="flex items-center gap-1">
                        <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                        <span className="text-sm">{config.rating}</span>
                    </div>
                </div>
                
                <div className="flex items-center justify-between">
                    <div>
                        <span className="text-2xl font-bold">${config.price}</span>
                        {config.nft_address && (
                            <Badge variant="secondary" className="ml-2">NFT</Badge>
                        )}
                    </div>
                    <div className="flex gap-2">
                        <Button size="sm" variant="outline" onClick={() => onPreview(config)}>
                            Preview
                        </Button>
                        <Button size="sm" onClick={() => onPurchase(config)}>
                            Buy Now
                        </Button>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
```

### Payment Processing
```tsx
// components/PaymentModal.tsx
export default function PaymentModal({ config, isOpen, onClose }) {
    const [paymentMethod, setPaymentMethod] = useState('stripe');
    const [isProcessing, setIsProcessing] = useState(false);
    
    const handleStripePayment = async () => {
        setIsProcessing(true);
        
        try {
            const { data } = await fetch('/api/payments/create-stripe-session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    configId: config.id,
                    priceId: config.stripe_price_id
                })
            }).then(res => res.json());
            
            // Redirect to Stripe Checkout
            window.location.href = data.checkout_url;
        } catch (error) {
            toast.error('Payment failed. Please try again.');
        } finally {
            setIsProcessing(false);
        }
    };
    
    const handleCryptoPayment = async () => {
        setIsProcessing(true);
        
        try {
            // Initialize Coinbase Commerce
            const charge = await fetch('/api/payments/create-crypto-charge', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    configId: config.id,
                    amount: config.price,
                    currency: 'USD'
                })
            }).then(res => res.json());
            
            // Open Coinbase Commerce modal
            window.CoinbaseCommerce.showCheckout({
                checkoutId: charge.checkout_id,
                onSuccess: handlePaymentSuccess,
                onError: handlePaymentError
            });
        } catch (error) {
            toast.error('Crypto payment initialization failed.');
        } finally {
            setIsProcessing(false);
        }
    };
    
    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-md">
                <DialogHeader>
                    <DialogTitle>Purchase {config.title}</DialogTitle>
                    <DialogDescription>
                        Choose your payment method
                    </DialogDescription>
                </DialogHeader>
                
                <div className="space-y-6">
                    {/* Payment Method Selection */}
                    <div className="space-y-3">
                        <PaymentMethodOption 
                            value="stripe"
                            selected={paymentMethod === 'stripe'}
                            onSelect={setPaymentMethod}
                            icon="💳"
                            title="Credit/Debit Card"
                            description="Secure payment via Stripe"
                        />
                        
                        <PaymentMethodOption 
                            value="crypto"
                            selected={paymentMethod === 'crypto'}
                            onSelect={setPaymentMethod}
                            icon="₿"
                            title="Cryptocurrency"
                            description="Pay with BTC, ETH, USDC"
                        />
                    </div>
                    
                    {/* Price Display */}
                    <div className="bg-slate-50 p-4 rounded-lg">
                        <div className="flex justify-between items-center">
                            <span className="font-medium">{config.title}</span>
                            <span className="text-2xl font-bold">${config.price}</span>
                        </div>
                        {config.nft_address && (
                            <p className="text-sm text-slate-600 mt-2">
                                Includes NFT ownership certificate
                            </p>
                        )}
                    </div>
                    
                    {/* Purchase Button */}
                    <Button 
                        className="w-full" 
                        onClick={paymentMethod === 'stripe' ? handleStripePayment : handleCryptoPayment}
                        disabled={isProcessing}
                    >
                        {isProcessing ? (
                            <>
                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                Processing...
                            </>
                        ) : (
                            `Pay $${config.price}`
                        )}
                    </Button>
                </div>
            </DialogContent>
        </Dialog>
    );
}
```

---

## 🎨 **CREATOR DASHBOARD**

### Config Upload & Minting
```jsx
// pages/creator/upload.tsx
export default function ConfigUpload() {
    const [uploadData, setUploadData] = useState({
        title: '',
        description: '',
        category: '',
        price: '',
        files: [],
        mintAsNFT: false
    });
    
    const handleFileUpload = async (files) => {
        const formData = new FormData();
        files.forEach(file => formData.append('files', file));
        
        const response = await fetch('/api/creator/upload-files', {
            method: 'POST',
            body: formData
        });
        
        const { uploadedFiles } = await response.json();
        setUploadData(prev => ({ ...prev, files: uploadedFiles }));
    };
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Create config collection
        const configResponse = await fetch('/api/creator/create-collection', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(uploadData)
        });
        
        const { collection } = await configResponse.json();
        
        // Mint NFT if requested
        if (uploadData.mintAsNFT) {
            await mintConfigNFT(collection.id);
        }
        
        router.push('/creator/dashboard');
    };
    
    return (
        <div className="container mx-auto px-4 py-8">
            <Card className="max-w-2xl mx-auto">
                <CardHeader>
                    <CardTitle>Upload New Config Collection</CardTitle>
                    <CardDescription>
                        Share your MAO configurations with the community
                    </CardDescription>
                </CardHeader>
                
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Basic Info */}
                        <div className="space-y-4">
                            <Input 
                                placeholder="Collection Title"
                                value={uploadData.title}
                                onChange={(e) => setUploadData(prev => ({ 
                                    ...prev, title: e.target.value 
                                }))}
                                required
                            />
                            
                            <Textarea 
                                placeholder="Describe your config collection..."
                                value={uploadData.description}
                                onChange={(e) => setUploadData(prev => ({ 
                                    ...prev, description: e.target.value 
                                }))}
                                rows={4}
                            />
                            
                            <Select 
                                value={uploadData.category} 
                                onValueChange={(value) => setUploadData(prev => ({ 
                                    ...prev, category: value 
                                }))}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Select category" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="workflow">Workflows</SelectItem>
                                    <SelectItem value="tools">Tools</SelectItem>
                                    <SelectItem value="templates">Templates</SelectItem>
                                    <SelectItem value="integrations">Integrations</SelectItem>
                                </SelectContent>
                            </Select>
                            
                            <Input 
                                type="number"
                                placeholder="Price (USD)"
                                value={uploadData.price}
                                onChange={(e) => setUploadData(prev => ({ 
                                    ...prev, price: e.target.value 
                                }))}
                                min="0"
                                step="0.01"
                            />
                        </div>
                        
                        {/* File Upload */}
                        <div>
                            <Label>Config Files</Label>
                            <FileUploader 
                                onUpload={handleFileUpload}
                                acceptedTypes={['.json', '.py', '.md']}
                                maxFiles={10}
                            />
                        </div>
                        
                        {/* NFT Minting Option */}
                        <div className="flex items-center space-x-2">
                            <Checkbox 
                                id="mintNFT"
                                checked={uploadData.mintAsNFT}
                                onCheckedChange={(checked) => setUploadData(prev => ({ 
                                    ...prev, mintAsNFT: checked 
                                }))}
                            />
                            <Label htmlFor="mintNFT">
                                Mint as NFT (+$9.99 minting fee, enables royalties)
                            </Label>
                        </div>
                        
                        <Button type="submit" className="w-full">
                            Upload & Publish
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
```

---

## 🔐 **USER AUTHENTICATION**

### Integration with Existing Secure Login
```tsx
// lib/auth.ts
import { supabase } from './supabase';

export const authConfig = {
    providers: [
        {
            id: 'passkey',
            name: 'Passkey',
            type: 'credentials',
            credentials: {},
            async authorize(credentials) {
                try {
                    // Verify passkey with existing MAO auth system
                    const response = await fetch('/api/auth/verify-passkey', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(credentials)
                    });
                    
                    const user = await response.json();
                    return user.success ? user.data : null;
                } catch (error) {
                    return null;
                }
            }
        }
    ],
    callbacks: {
        async session({ session, token }) {
            // Add subscription info to session
            if (session.user?.email) {
                const { data: subscription } = await supabase
                    .from('subscriptions')
                    .select('tier, status')
                    .eq('user_id', token.sub)
                    .single();
                
                session.user.subscription = subscription;
            }
            return session;
        }
    }
};
```

---

## 💎 **SUCCESS METRICS & ROLLOUT**

### Revenue Targets
- **Month 1**: $10K MRR (333 Pro subscribers)
- **Month 3**: $50K MRR (1,666 Pro subscribers)  
- **Month 6**: $200K MRR (6,666 Pro subscribers)
- **Year 1**: $1M MRR (33,333 Pro subscribers)

### Key Features Rollout
1. **Week 1**: Basic storefront + Stripe integration
2. **Week 2**: Config marketplace + downloads
3. **Week 3**: Crypto payments + NFT minting
4. **Week 4**: Creator dashboard + revenue sharing

### Global Expansion
- **Phase 1**: English + Spanish markets
- **Phase 2**: Add Portuguese, French, German
- **Phase 3**: Asian markets (Chinese, Japanese, Korean)

---

## 🚀 **THE MONEY MACHINE**

This isn't just a website; it's a **global subscription empire** that turns MAO configs into recurring revenue. With multilingual support, crypto payments, and NFT-powered creator economy, we're building the **GitHub of AI workflows** with actual monetization.

**Ready to print money?** 💰🚀 