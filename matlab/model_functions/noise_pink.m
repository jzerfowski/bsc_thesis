function [Ie_noise, Ii_noise] = noise_pink(dt, reg, tnumb, noiseseed, noiseamp, noisecor, Ienoise, Iinoise)

s = RandStream('mcg16807','Seed', noiseseed);
RandStream.setGlobalStream(s);

B = [0.049922035 -0.095993537 0.050612699 -0.004408786];
A = [1 -2.494956002   2.017265875  -0.522189400];
nsigp = zeros(reg, tnumb);
for r = 1:reg
    randsig = noiseamp * 2*randn(1,tnumb);
    nsigp(r,:) = filter(B,A,randsig);
end

nsigp(reg,:) = noisecor*nsigp(1,:) + (1-noisecor)*nsigp(reg,:);
Ii_noise = single(bsxfun(@times,Iinoise(1:reg)',nsigp)); 
Ie_noise = single(bsxfun(@times,Ienoise(1:reg)',nsigp));
clear nsigp

end